import { useEffect, useRef, useState } from "react";
import { Clip, Close, Mic, Send } from "../lib/icons.jsx";

const ACCEPT = "image/*,.pdf,.doc,.docx,.xlsx,.txt";

export default function Composer({ pending, onSend, onStop, speech }) {
  const [value, setValue] = useState("");
  const [files, setFiles] = useState([]);
  const fieldRef = useRef(null);
  const fileRef = useRef(null);

  useEffect(() => {
    const field = fieldRef.current;
    if (!field) return;
    field.style.height = "auto";
    field.style.height = `${Math.min(field.scrollHeight, 200)}px`;
  }, [value]);

  const submit = () => {
    if (pending) return;
    const text = value.trim();
    if (!text && files.length === 0) return;
    onSend(text, files);
    setValue("");
    setFiles([]);
    if (fileRef.current) fileRef.current.value = "";
  };

  const onKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      submit();
    }
  };

  const addFiles = (event) => {
    setFiles((current) => [...current, ...Array.from(event.target.files ?? [])].slice(0, 2));
  };

  return (
    <div className="composer">
      {files.length > 0 && (
        <div className="composer__attachments">
          {files.map((file) => (
            <span className="chip" key={file.name}>
              <span>{file.name}</span>
              <button
                type="button"
                onClick={() => setFiles((current) => current.filter((f) => f !== file))}
                aria-label={`Retirer ${file.name}`}
              >
                <Close width="13" height="13" />
              </button>
            </span>
          ))}
        </div>
      )}

      <div className="composer__box">
        <input
          ref={fileRef}
          type="file"
          accept={ACCEPT}
          multiple
          hidden
          onChange={addFiles}
        />

        <button
          type="button"
          className="icon-button"
          onClick={() => fileRef.current?.click()}
          aria-label="Joindre une image ou un document"
          title="Joindre un fichier"
        >
          <Clip />
        </button>

        {speech.supported && (
          <button
            type="button"
            className="icon-button mic"
            data-active={speech.listening}
            onClick={speech.toggle}
            aria-pressed={speech.listening}
            aria-label={speech.listening ? "Arrêter la dictée" : "Dicter un message"}
            title="Dicter"
          >
            <Mic />
          </button>
        )}

        <textarea
          ref={fieldRef}
          className="composer__field"
          rows={1}
          value={value}
          placeholder="Écris ton message"
          onChange={(event) => setValue(event.target.value)}
          onKeyDown={onKeyDown}
          aria-label="Message"
        />

        <button
          type="button"
          className="composer__send"
          onClick={pending ? onStop : submit}
          disabled={!pending && !value.trim() && files.length === 0}
          aria-label={pending ? "Arrêter la réponse" : "Envoyer le message"}
        >
          {pending ? <Close width="15" height="15" /> : <Send />}
        </button>
      </div>

      <p className="composer__hint">
        Entrée envoie, Maj+Entrée saute une ligne. Commandes : /image, /pdf, /doc, /excel.
      </p>
    </div>
  );
}
