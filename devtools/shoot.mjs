// shoot.mjs <out-dir> [light|dark] [viewer-url]: screenshots every view and step of the deck served on localhost:8000
// (./serve.sh --no-open; DECK_URL overrides the deck address, e.g. http://localhost:8001); needs GR4_PRESENT set to a gr4-present checkout, and `node --experimental-websocket` on Node 20
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

// an import specifier cannot be computed, so the harness is loaded dynamically from the checkout GR4_PRESENT names
const harness = path.resolve(process.env.GR4_PRESENT ?? path.join(path.dirname(new URL(import.meta.url).pathname), "../../gr4-present"), "devtools/browser_harness.mjs");
const { launchBrowser, openPage } = await import(pathToFileURL(harness).href);

const out = process.argv[2] ?? "shots/light";
const theme = process.argv[3] ?? "light";
const viewer = process.argv[4] ?? "https://ralphsteinhagen.github.io/gr4-present/";
await mkdir(out, { recursive: true });
const browser = await launchBrowser(["--window-size=1600,900", "--disable-features=LocalNetworkAccessChecks,PrivateNetworkAccessRespectPreflightResults,PrivateNetworkAccessSendPreflights", `--force-color-profile=srgb`]);
const log = [];
try {
  const deck = process.env.DECK_URL ?? "http://localhost:8000";
  const url = `${viewer}?presentation=${encodeURIComponent(deck)}&theme=${theme}`;
  const page = await openPage(browser, url);
  log.push(`opened ${url}`);
  // the window size is advisory under some drivers; the viewport is pinned to the deck's 16:9 so the shots show the layout the room sees
  await page.command("Emulation.setDeviceMetricsOverride", { width: 1600, height: 900, deviceScaleFactor: 1, mobile: false });
  if (theme === "dark") {
    // the viewer follows prefers-color-scheme; emulate it and reload so the runtime starts under it
    await page.command("Emulation.setEmulatedMedia", { features: [{ name: "prefers-color-scheme", value: "dark" }] }); // persists across the service worker's reload
  }
  log.push(`isolated: ${await page.waitFor("window.crossOriginIsolated === true", 90_000)}`);
  log.push(`launched: ${await page.waitFor("!!document.getElementById('launch')?.classList.contains('done')", 120_000)}`);
  await page.waitFor("(document.getElementById('canvas')?.width ?? 0) > 0");
  await page.waitFor("(globalThis.gr4Location || '').includes('view=')", 120_000);
  await page.evaluate("document.getElementById('canvas').focus()");
  await new Promise((r) => setTimeout(r, 3000));
  let location = await page.evaluate("globalThis.gr4Location || ''");
  for (let shot = 0; shot < 150; ++shot) {
    await new Promise((r) => setTimeout(r, 1200)); // fades and image decoding
    const file = path.join(out, `${String(shot).padStart(3, "0")}-${location.replace(/[^a-z0-9=&-]/gi, "_")}.png`);
    await page.screenshot(file);
    log.push(`${shot}: ${location}`);
    await page.press("ArrowRight", "ArrowRight", 39);
    let next = location;
    try {
      next = await page.waitFor(`(globalThis.gr4Location || '') !== ${JSON.stringify(location)} ? (globalThis.gr4Location || '') : false`, 8000);
    } catch {
      break; // the last view
    }
    location = next;
  }
  await writeFile(path.join(out, "console.txt"), page.consoleLines.join("\n"));
  await page.close();
} catch (error) {
  log.push(`error: ${error.message}`);
} finally {
  await browser.stop();
  await writeFile(path.join(out, "log.txt"), log.join("\n"));
  console.log(log.join("\n"));
}
