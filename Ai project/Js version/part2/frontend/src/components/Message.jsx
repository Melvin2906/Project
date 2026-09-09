import { memo, useMemo, useState } from "react";
import { renderMarkdown } from "../lib/markdown.js";
import { Copy, Speaker } from "../lib/icons.jsx";

function UserMessage({ message }) {
  return (
    <div className="msg msg--user">
      {message.content}
      {message.files?.length > 0 && (
        <div className="composer__attachments" style={{ marginTop: 8, marginBottom: 0 }}>
          {message.files.map((name) => (
            <span className="chip" key={name}>
              <span>{name}</span>
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

function AssistantMessage({ message, onSpeak }) {
  const [copied, setCopied] = useState(false);

  const html = useMemo(
    () => (message.kind ? null : renderMarkdown(message.content ?? "")),
    [message.content, message.kind]
  );

  const copy = async () => {
    await navigator.clipboard.writeText(message.content ?? "");
    setCopied(true);
    setTimeout(() => setCopied(false), 1600);
  };

  return (
    <div className={`msg msg--assistant${message.error ? " msg--error" : ""}`}>
      {message.kind === "image" && (
        <div className="msg__body">
          <img src={message.url} alt="Image générée à partir de ta demande" />
        </div>
      )}

      {message.kind === "file" && (
        <div className="msg__body">
          <a href={message.url} download={message.filename}>
            Télécharger {message.filename}
          </a>
        </div>
      )}

      {html !== null && <div className="msg__body" dangerouslySetInnerHTML={{ __html: html }} />}

      {!message.error && !message.kind && (
        <div className="msg__tools">
          <button type="button" className="msg__tool" onClick={copy}>
            <Copy /> {copied ? "Copié" : "Copier"}
          </button>
          <button type="button" className="msg__tool" onClick={() => onSpeak(message.content)}>
            <Speaker /> Lire
          </button>
        </div>
      )}
    </div>
  );
}

function Message({ message, onSpeak }) {
  return message.role === "user" ? (
    <UserMessage message={message} />
  ) : (
    <AssistantMessage message={message} onSpeak={onSpeak} />
  );
}

export default memo(Message);
