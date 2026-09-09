/* Icônes SVG inline : colorables en CSS, nettes partout, zéro requête. */

const base = {
  width: 18,
  height: 18,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.7,
  strokeLinecap: "round",
  strokeLinejoin: "round",
  "aria-hidden": true,
};

export const Plus = (p) => (
  <svg {...base} {...p}><path d="M12 5v14M5 12h14" /></svg>
);

export const Panel = (p) => (
  <svg {...base} {...p}><rect x="3" y="4" width="18" height="16" rx="2" /><path d="M9 4v16" /></svg>
);

export const Trash = (p) => (
  <svg {...base} {...p} width="15" height="15"><path d="M4 7h16M10 11v6M14 11v6M6 7l1 12a2 2 0 002 2h6a2 2 0 002-2l1-12M9 7V5a1 1 0 011-1h4a1 1 0 011 1v2" /></svg>
);

export const Clip = (p) => (
  <svg {...base} {...p}><path d="M21 11.5l-8.6 8.6a5 5 0 01-7-7l9-9a3.4 3.4 0 014.8 4.8l-9 9a1.8 1.8 0 01-2.5-2.5l8.2-8.2" /></svg>
);

export const Mic = (p) => (
  <svg {...base} {...p}><rect x="9" y="3" width="6" height="11" rx="3" /><path d="M5 11a7 7 0 0014 0M12 18v3" /></svg>
);

export const Send = (p) => (
  <svg {...base} {...p} width="17" height="17"><path d="M5 12h13M12 5l7 7-7 7" /></svg>
);

export const Copy = (p) => (
  <svg {...base} {...p} width="15" height="15"><rect x="9" y="9" width="11" height="11" rx="2" /><path d="M5 15V5a2 2 0 012-2h8" /></svg>
);

export const Speaker = (p) => (
  <svg {...base} {...p} width="15" height="15"><path d="M11 5L6 9H3v6h3l5 4V5zM16 9a4 4 0 010 6" /></svg>
);

export const Close = (p) => (
  <svg {...base} {...p}><path d="M6 6l12 12M18 6L6 18" /></svg>
);

export const Gear = (p) => (
  <svg {...base} {...p}><circle cx="12" cy="12" r="3.2" /><path d="M12 3v2.2M12 18.8V21M4.2 7.5l1.9 1.1M17.9 15.4l1.9 1.1M4.2 16.5l1.9-1.1M17.9 8.6l1.9-1.1" /></svg>
);
