#!/usr/bin/env python3
"""Migrate remote audio to GitHub repo; never mark missing/corrupted downloads local."""
import json, urllib.request, urllib.error, pathlib, subprocess, re, os
root=pathlib.Path(__file__).resolve().parents[1]
catalog=root/"data/tracks.json"
obj=json.loads(catalog.read_text(encoding="utf-8"))
report=[]
for item in obj["tracks"]:
    url=item.get("src","")
    if not url.startswith("https://"):
        report.append({"id":item["id"],"status":"already-local"});continue
    ext=pathlib.Path(urllib.request.urlparse(url).path).suffix.lower() if hasattr(urllib.request,"urlparse") else ""
    if not ext or ext not in (".mp3",".ogg",".flac",".wav",".m4a"):
        ext={"freely-tomorrow":".ogg"}.get(item["id"],".mp3")
    category="vocaloid" if item.get("category")=="Vocaloid" else "game-ost"
    target=pathlib.Path("music")/category/(re.sub(r"[^a-zA-Z0-9_-]","-",item["id"])+ext)
    dest=root/target
    dest.parent.mkdir(parents=True,exist_ok=True)
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"AnimeMusicArchive/1.0 (GitHub Actions music archiver)"})
        with urllib.request.urlopen(req,timeout=75) as response:
            ct=response.headers.get("content-type","").lower()
            if "text/html" in ct: raise ValueError("HTML rather than audio")
            with dest.open("wb") as out:
                size=0
                while True:
                    chunk=response.read(1024*512)
                    if not chunk:break
                    size+=len(chunk)
                    if size>95*1024*1024:raise ValueError("file too large")
                    out.write(chunk)
        if dest.stat().st_size<150000:raise ValueError("audio too small")
        p=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(dest)],capture_output=True,text=True,timeout=25)
        if p.returncode:raise ValueError("ffprobe failed: "+p.stderr[:90])
        seconds=float(p.stdout.strip())
        if seconds<70:raise ValueError(f"only {seconds:.0f}s, likely a sample")
        item["src"]=target.as_posix()
        item["duration"]=round(seconds)
        item["storage"]="github-repository"
        report.append({"id":item["id"],"status":"migrated","bytes":dest.stat().st_size,"duration":round(seconds),"path":target.as_posix()})
    except Exception as err:
        dest.unlink(missing_ok=True)
        report.append({"id":item["id"],"status":"failed","reason":str(err)[:250]})
obj["migration_report"]="data/migration-report.json"
catalog.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(root/"data/migration-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
