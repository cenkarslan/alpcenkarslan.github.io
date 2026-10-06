// Kareleri Playwright/Chromium ile üretir, ffmpeg ile MP4'e çevirir.
// Kullanım:
//   node render.mjs                     → tam video (out/putin-valdai-2026-ai-analiz.mp4)
//   node render.mjs --stills 2.2,8,17.5 → yalnızca test kareleri (out/stills/*.png)
//   node render.mjs --plate kaynak.mp4  → kaynak karesine gerçek konuşma görüntüsü
import { chromium } from "playwright";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const DIR = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = k => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null; };
const FPS = 30, DUR = 60, WORKERS = +(opt("--workers") || 4);
const OUT = path.join(DIR, "out");
const FRAMES = opt("--frames") || path.join(OUT, "frames");
const stills = opt("--stills");
const plate = opt("--plate");

const MIME = { ".html": "text/html", ".otf": "font/otf", ".ttf": "font/ttf", ".mp4": "video/mp4", ".webm": "video/webm", ".js": "text/javascript" };
const server = http.createServer((req, res) => {
  const p = path.join(DIR, decodeURIComponent(req.url.split("?")[0]));
  if (!p.startsWith(DIR) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { "Content-Type": MIME[path.extname(p)] || "application/octet-stream" });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const port = server.address().port;
const url = `http://127.0.0.1:${port}/index.html?render${plate ? "&plate=" + encodeURIComponent(plate) : ""}`;

const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium", args: ["--autoplay-policy=no-user-gesture-required"] }).catch(() => chromium.launch());
async function newPage() {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on("console", m => console.log("[page]", m.text()));
  page.on("pageerror", e => console.error("[pageerror]", e.message));
  await page.goto(url);
  await page.waitForFunction(() => window.READY === true, null, { timeout: 60000 });
  return page;
}
const grab = (page, t, type) => page.evaluate(async ([t, type]) => {
  await window.renderFrame(t);
  return document.getElementById("c").toDataURL(type, 0.95).split(",")[1];
}, [t, type]);

if (stills) {
  const dir = path.join(OUT, "stills"); fs.mkdirSync(dir, { recursive: true });
  const page = await newPage();
  console.log("Alt-üç satır sayıları:", JSON.stringify(await page.evaluate(() => window.LT_CHECK())));
  for (const s of stills.split(",")) {
    const b64 = await grab(page, +s, "image/png");
    fs.writeFileSync(path.join(dir, `t${(+s).toFixed(2).padStart(5, "0")}.png`), Buffer.from(b64, "base64"));
  }
  console.log("stills →", dir);
} else {
  fs.mkdirSync(FRAMES, { recursive: true });
  const N = FPS * DUR; let done = 0; const t0 = Date.now();
  await Promise.all(Array.from({ length: WORKERS }, async (_, w) => {
    const page = await newPage();
    for (let i = w; i < N; i += WORKERS) {
      const b64 = await grab(page, i / FPS, "image/jpeg");
      fs.writeFileSync(path.join(FRAMES, `f${String(i).padStart(5, "0")}.jpg`), Buffer.from(b64, "base64"));
      if (++done % 150 === 0) console.log(`${done}/${N} kare · ${((Date.now() - t0) / 1000).toFixed(0)} sn`);
    }
  }));
  const audio = path.join(DIR, "audio", "soundtrack.wav");
  const mp4 = path.join(OUT, "putin-valdai-2026-ai-analiz.mp4");
  const ff = ["-y", "-framerate", String(FPS), "-i", path.join(FRAMES, "f%05d.jpg")];
  if (fs.existsSync(audio)) ff.push("-i", audio, "-c:a", "aac", "-b:a", "192k", "-shortest");
  ff.push("-c:v", "libx264", "-preset", "slow", "-crf", "19", "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart", mp4);
  const r = spawnSync("ffmpeg", ff, { stdio: "inherit" });
  if (r.status !== 0) process.exitCode = 1; else console.log("video →", mp4);
}
await browser.close(); server.close();
