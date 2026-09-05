export function openAIFocus({
  kind = "module",
  target,
  title = "Selected finding",
  question = "Explain this finding and tell me how I should address it safely.",
  smellType = "",
}) {
  window.dispatchEvent(new CustomEvent("forgeiq:ai-focus", {
    detail: { kind, target, title, question, smellType },
  }));
}
