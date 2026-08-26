import React from 'react';
import { Search, Volume2, VolumeX, Share2, RefreshCw, Sparkles } from 'lucide-react';

export default function Header({ 
  onRerollAll, 
  onOpenSearch, 
  onExportMarkdown, 
  soundEnabled, 
  setSoundEnabled,
  isRolling 
}) {
  return (
    <header className="border-b border-amber-500/25 bg-[#0a0f1d]/95 backdrop-blur-lg sticky top-0 z-30 shadow-xl">
      <div className="max-w-[1750px] mx-auto px-6 py-4 sm:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
        
        {/* Left Branding */}
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-amber-400 to-amber-700 p-0.5 shadow-xl shadow-amber-500/20 flex items-center justify-center flex-shrink-0">
            <div className="w-full h-full bg-[#0d1222] rounded-[10px] flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-amber-400 animate-pulse" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2.5 flex-wrap">
              <h1 className="font-cinzel text-xl sm:text-2xl lg:text-3xl font-black tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-amber-200 via-amber-400 to-yellow-500">
                WARFRAME EDA / ETA LOADOUT
              </h1>
              <span className="text-xs uppercase font-extrabold tracking-widest px-2.5 py-0.5 rounded-md bg-amber-950/90 text-amber-300 border border-amber-500/50 shadow-sm">
                3 OF EACH
              </span>
            </div>
            <p className="text-xs sm:text-sm text-slate-400 flex items-center gap-2 mt-0.5">
              <span>3 Warframes • 3 Primaries • 3 Secondaries • 3 Melees</span>
              <span className="text-amber-500/60">•</span>
              <span className="text-amber-300 font-semibold">wiki.warframe.com</span>
            </p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center flex-wrap justify-center gap-3">
          
          {/* Wiki Search Modal Trigger */}
          <button
            onClick={onOpenSearch}
            className="flex items-center gap-2.5 px-4 py-2.5 rounded-xl bg-slate-800/90 hover:bg-slate-700 text-slate-200 text-sm font-semibold border border-slate-700 transition-all hover:border-amber-500/60 shadow-md"
            title="Search Official Warframe Wiki (Press /)"
          >
            <Search className="w-4 h-4 text-amber-400" />
            <span>Search Wiki</span>
            <kbd className="hidden sm:inline-block px-2 py-0.5 text-xs bg-slate-900 text-slate-400 rounded-md border border-slate-700 font-mono">
              /
            </kbd>
          </button>

          {/* Sound Toggle */}
          <button
            onClick={() => setSoundEnabled(!soundEnabled)}
            className={`p-2.5 rounded-xl text-sm font-medium border transition-all shadow-md ${
              soundEnabled 
                ? 'bg-amber-950/40 border-amber-500/50 text-amber-300 hover:bg-amber-900/50' 
                : 'bg-slate-800/70 border-slate-700 text-slate-400 hover:text-slate-200'
            }`}
            title={soundEnabled ? "Mute SFX" : "Enable SFX"}
          >
            {soundEnabled ? <Volume2 className="w-5 h-5" /> : <VolumeX className="w-5 h-5" />}
          </button>

          {/* Export / Share */}
          <button
            onClick={onExportMarkdown}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800/90 hover:bg-slate-700 text-slate-200 text-sm font-semibold border border-slate-700 hover:border-cyan-500/60 transition-all shadow-md"
            title="Copy Discord / Markdown loadout to clipboard"
          >
            <Share2 className="w-4 h-4 text-cyan-400" />
            <span>Export</span>
          </button>

          {/* Reroll All */}
          <button
            onClick={onRerollAll}
            disabled={isRolling}
            className="flex items-center gap-2.5 px-5 py-2.5 rounded-xl bg-gradient-to-r from-amber-500 to-yellow-600 hover:from-amber-400 hover:to-yellow-500 text-slate-950 font-black text-sm shadow-xl shadow-amber-500/25 hover:shadow-amber-500/40 transition-all disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${isRolling ? 'animate-spin' : ''}`} />
            <span>REROLL ALL</span>
          </button>
        </div>

      </div>
    </header>
  );
}
