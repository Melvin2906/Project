import { marked } from "marked";
import DOMPurify from "dompurify";

marked.setOptions({ breaks: true, gfm: true });

/** Markdown du modèle -> HTML sûr. Les liens s'ouvrent hors de la page. */
export function renderMarkdown(source = "") {
  const html = marked.parse(source);
  return DOMPurify.sanitize(html, { ADD_ATTR: ["target", "rel"] });
}

DOMPurify.addHook("afterSanitizeAttributes", (node) => {
  if (node.tagName === "A") {
    node.setAttribute("target", "_blank");
    node.setAttribute("rel", "noopener noreferrer");
  }
});
