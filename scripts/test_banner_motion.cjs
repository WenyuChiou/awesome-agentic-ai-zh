/* Browser-state tests using only Node's standard library. */
const assert = require("node:assert/strict");
const { readFileSync } = require("node:fs");
const { join } = require("node:path");
const { test } = require("node:test");
const vm = require("node:vm");

const source = readFileSync(join(__dirname, "../docs/javascripts/banner-motion.js"), "utf8");

function banner({ role = false } = {}) {
  const basename = role ? "branch-decision-tree" : "banner";
  const attributes = { src: `../resources/diagrams/${basename}.en.png` };
  const image = {
    writes: 0,
    getAttribute: (name) => attributes[name],
    setAttribute(name, value) { attributes[name] = value; this.writes += 1; },
  };
  const original = { setAttribute(name, value) { this[name] = value; } };
  const imageLink = role ? { setAttribute(name, value) { this[name] = value; } } : null;
  const button = { hidden: true, disabled: false };
  const element = {
    dataset: {
      staticSrc: attributes.src, animatedSrc: `../resources/diagrams/${basename}.en.svg`,
      playLabel: "Play animation", stopLabel: "Stop animation",
      reducedLabel: "Animation disabled: reduced motion is on",
    },
    querySelector: (selector) => ({ img: image, ".aaz-banner__toggle": button, ".aaz-banner__original": original, ".aaz-diagram__image-link": imageLink })[selector],
  };
  button.closest = (selector) => selector === ".aaz-banner" ? element : button;
  return { element, image, button, original, imageLink };
}

function browser({ reduced = false, loading = false, instant = true } = {}) {
  const listeners = {};
  const mediaListeners = [];
  const subscribers = [];
  const first = banner();
  const media = { matches: reduced, addEventListener: (event, callback) => mediaListeners.push(callback) };
  const document = {
    readyState: loading ? "loading" : "complete", banners: [first.element],
    querySelectorAll() { return this.banners; },
    addEventListener(event, callback) { (listeners[event] ??= []).push(callback); },
  };
  const context = vm.createContext({ window: { matchMedia: () => media }, document });
  if (instant) context.document$ = { subscribe: (callback) => { subscribers.push(callback); callback(); } };
  vm.runInContext(source, context);
  return {
    ...first, context, document, listeners, mediaListeners, subscribers,
    click() { listeners.click.forEach((callback) => callback({ target: this.button })); },
    setReduced(value) { media.matches = value; mediaListeners.forEach((callback) => callback()); },
    navigate(next) { document.banners = [next.element]; subscribers.forEach((callback) => callback()); },
  };
}

test("normal motion swaps one image and full-size target; stop and play stay accurate", () => {
  const page = browser();
  assert.equal(page.image.getAttribute("src"), page.element.dataset.animatedSrc);
  assert.equal(page.original.href, page.element.dataset.animatedSrc);
  assert.equal(page.button.textContent, "Stop animation");
  assert.equal(page.button.hidden, false);
  assert.equal(page.image.writes, 1);
  page.click();
  assert.equal(page.image.getAttribute("src"), page.element.dataset.staticSrc);
  assert.equal(page.original.href, page.element.dataset.staticSrc);
  assert.equal(page.button.textContent, "Play animation");
  page.click();
  assert.equal(page.image.getAttribute("src"), page.element.dataset.animatedSrc);
});

test("reduced motion starts static, explains disabled play, and follows system changes", () => {
  const page = browser({ reduced: true });
  assert.equal(page.image.getAttribute("src"), page.element.dataset.staticSrc);
  assert.equal(page.image.writes, 0);
  assert.equal(page.button.disabled, true);
  assert.equal(page.button.textContent, page.element.dataset.reducedLabel);
  page.click();
  assert.equal(page.image.writes, 0);
  page.setReduced(false);
  assert.equal(page.image.getAttribute("src"), page.element.dataset.animatedSrc);
  assert.equal(page.button.disabled, false);
  assert.equal(page.button.textContent, "Stop animation");
  page.setReduced(true);
  assert.equal(page.image.getAttribute("src"), page.element.dataset.staticSrc);
});

test("instant navigation preserves manual stop and never retains detached banner images", () => {
  const page = browser();
  page.click();
  const next = banner();
  page.navigate(next);
  assert.equal(next.image.getAttribute("src"), next.element.dataset.staticSrc);
  assert.equal(next.button.textContent, "Play animation");
  const oldWrites = page.image.writes;
  page.setReduced(true);
  page.setReduced(false);
  assert.equal(next.image.getAttribute("src"), next.element.dataset.staticSrc);
  assert.equal(page.image.writes, oldWrites);
  page.listeners.click[0]({ target: next.button });
  assert.equal(next.image.getAttribute("src"), next.element.dataset.animatedSrc);
});

test("repeated script execution and instant navigation add no duplicate listeners", () => {
  const page = browser();
  vm.runInContext(source, page.context);
  page.navigate(page);
  page.navigate(page);
  assert.equal(page.listeners.click.length, 1);
  assert.equal(page.mediaListeners.length, 1);
  assert.equal(page.subscribers.length, 1);
  assert.equal(page.image.writes, 1);
  page.click();
  assert.equal(page.image.getAttribute("src"), page.element.dataset.staticSrc);
});

test("standalone DOM-ready initialization works without Material document$", () => {
  const page = browser({ loading: true, instant: false });
  assert.equal(page.button.hidden, true);
  page.listeners.DOMContentLoaded[0]();
  assert.equal(page.button.hidden, false);
  assert.equal(page.button.textContent, "Stop animation");
});

test("role figures update both full-size links and share pause and reduced-motion state", () => {
  const page = browser();
  const role = banner({ role: true });
  page.document.banners.push(role.element);
  page.subscribers[0]();
  for (const asset of [page, role]) {
    assert.equal(asset.image.getAttribute("src"), asset.element.dataset.animatedSrc);
    assert.equal(asset.original.href, asset.element.dataset.animatedSrc);
  }
  assert.equal(role.imageLink.href, role.element.dataset.animatedSrc);
  page.listeners.click[0]({ target: role.button });
  for (const asset of [page, role]) {
    assert.equal(asset.image.getAttribute("src"), asset.element.dataset.staticSrc);
    assert.equal(asset.original.href, asset.element.dataset.staticSrc);
    assert.equal(asset.button.textContent, "Play animation");
  }
  assert.equal(role.imageLink.href, role.element.dataset.staticSrc);
  page.setReduced(true);
  assert.equal(role.button.disabled, true);
  assert.equal(role.button.textContent, role.element.dataset.reducedLabel);
  page.setReduced(false);
  page.click();
  assert.equal(role.imageLink.href, role.element.dataset.animatedSrc);
  page.setReduced(true);
  assert.equal(role.imageLink.href, role.element.dataset.staticSrc);
});
