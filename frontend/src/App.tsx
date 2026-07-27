import React from 'react'

export default function App() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4 text-center bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      <div className="max-w-xl p-8 rounded-2xl bg-slate-900/60 backdrop-blur-xl border border-slate-800 shadow-2xl">
        <h1 className="text-5xl font-extrabold tracking-tight bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent mb-4">
          ProjectIQ
        </h1>
        <p className="text-xl font-medium text-slate-300 mb-6">
          Know your code before you clone it.
        </p>
        <div className="inline-block px-4 py-2 text-sm font-semibold rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
          Coming Soon
        </div>
      </div>
    </div>
  )
}
