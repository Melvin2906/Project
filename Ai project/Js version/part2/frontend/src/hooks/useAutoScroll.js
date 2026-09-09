import { useEffect, useRef, useState } from "react";

/**
 * Colle le fil de discussion en bas tant que l'utilisateur n'a pas
 * remonté lui-même. Corrige le défaut principal de l'ancien front :
 * la réponse arrivait hors écran.
 */
export function useAutoScroll(deps) {
  const ref = useRef(null);
  const [atBottom, setAtBottom] = useState(true);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;
    const onScroll = () => {
      const gap = node.scrollHeight - node.scrollTop - node.clientHeight;
      setAtBottom(gap < 80);
    };
    node.addEventListener("scroll", onScroll, { passive: true });
    return () => node.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    const node = ref.current;
    if (node && atBottom) node.scrollTop = node.scrollHeight;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return { ref, atBottom };
}
