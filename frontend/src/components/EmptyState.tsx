interface Props {
  icon?: string;
  title: string;
  message: string;
  actionLabel?: string;
  onAction?: () => void;
}

export function EmptyState({ icon = "🥕", title, message, actionLabel, onAction }: Props) {
  return (
    <div className="empty-state">
      <div className="empty-icon" aria-hidden>{icon}</div>
      <h3>{title}</h3>
      <p>{message}</p>
      {actionLabel && onAction && (
        <button className="primary" onClick={onAction} type="button">
          {actionLabel}
        </button>
      )}
    </div>
  );
}
