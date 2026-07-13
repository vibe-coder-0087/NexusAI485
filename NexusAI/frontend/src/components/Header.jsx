export default function Header({ title, subtitle }) {
  return (
    <div className="mb-6">
      <h1 className="font-display text-2xl font-semibold text-white tracking-tight">{title}</h1>
      {subtitle && <p className="text-sm text-gray-500 mt-1 max-w-2xl">{subtitle}</p>}
    </div>
  )
}
