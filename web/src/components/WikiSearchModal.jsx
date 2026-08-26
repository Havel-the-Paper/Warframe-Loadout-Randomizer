import React, { useState, useMemo, useEffect, useRef } from 'react';
import { Search, X, ExternalLink, Sparkles } from 'lucide-react';

export default function WikiSearchModal({ isOpen, onClose, allItems }) {
  const [query, setQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const inputRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    } else {
      setQuery('');
    }
  }, [isOpen]);

  useEffect(() => {
    function handleKeyDown(e) {
      if (e.key === '/' && !isOpen && document.activeElement.tagName !== 'INPUT') {
        e.preventDefault();
        onClose(false);
      }
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    }
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  const filteredItems = useMemo(() => {
    const q = query.trim().toLowerCase();
    
    return allItems.filter(item => {
      if (selectedCategory !== 'All') {
        if (selectedCategory === 'Warframes' && item.category !== 'Warframe') return false;
        if (selectedCategory === 'Primary' && item.category !== 'Primary') return false;
        if (selectedCategory === 'Secondary' && item.category !== 'Secondary') return false;
        if (selectedCategory === 'Melee' && item.category !== 'Melee') return false;
      }

      if (!q) return true;

      const nameMatch = item.name.toLowerCase().includes(q);
      const typeMatch = item.type.toLowerCase().includes(q);
      const descMatch = (item.description || '').toLowerCase().includes(q);

      return nameMatch || typeMatch || descMatch;
    }).slice(0, 40);
  }, [allItems, query, selectedCategory]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-in fade-in duration-200">
      
      {/* Modal Container */}
      <div 
        className="w-full max-w-4xl bg-[#0b0f1d] border-2 border-amber-500/50 rounded-3xl shadow-2xl shadow-amber-500/20 flex flex-col max-h-[85vh] overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        
        {/* Search Header Bar */}
        <div className="p-5 border-b border-slate-800 bg-[#0e1426] flex items-center gap-4">
          <Search className="w-6 h-6 text-amber-400 flex-shrink-0" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search Warframes, Primaries, Secondaries, Melee on wiki.warframe.com..."
            className="w-full bg-transparent text-slate-100 placeholder-slate-500 text-base sm:text-lg focus:outline-none font-semibold"
          />
          {query && (
            <button 
              onClick={() => setQuery('')}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800"
            >
              <X className="w-5 h-5" />
            </button>
          )}
          <button
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-800 border border-slate-700"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Filter Pills Bar */}
        <div className="px-5 py-3 bg-slate-950/70 border-b border-slate-800 flex items-center justify-between gap-3 overflow-x-auto">
          
          {/* Category Tabs */}
          <div className="flex items-center gap-2 flex-shrink-0">
            {['All', 'Warframes', 'Primary', 'Secondary', 'Melee'].map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-bold transition-all ${
                  selectedCategory === cat
                    ? 'bg-amber-500 text-slate-950 shadow-md'
                    : 'bg-slate-900 text-slate-400 hover:text-slate-200 hover:bg-slate-800 border border-slate-800'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          <span className="text-xs text-amber-400/80 font-mono hidden sm:inline font-bold">
            wiki.warframe.com
          </span>
        </div>

        {/* Results List */}
        <div className="p-5 overflow-y-auto flex-1 divide-y divide-slate-800/80 space-y-3">
          {filteredItems.length === 0 ? (
            <div className="py-16 text-center text-slate-500">
              <Search className="w-12 h-12 mx-auto mb-4 opacity-30 text-amber-400" />
              <p className="text-base font-bold text-slate-400">No equipment found matching "{query}"</p>
              <p className="text-xs sm:text-sm text-slate-600 mt-1">Try searching for Saryn, Braton, Lex, Nikana, etc.</p>
            </div>
          ) : (
            filteredItems.map((item) => (
              <div 
                key={item.name}
                className="pt-3 pb-3 flex items-center justify-between gap-4 group hover:bg-slate-900/60 p-3 rounded-xl transition-colors"
              >
                {/* Thumbnail & Title */}
                <div className="flex items-center gap-4 min-w-0">
                  <div className="w-16 h-16 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-center p-2 flex-shrink-0 group-hover:border-amber-500/40">
                    {item.imageUrl ? (
                      <img 
                        src={item.imageUrl} 
                        alt={item.name} 
                        className="w-full h-full object-contain"
                        onError={(e) => { e.target.style.display = 'none'; }}
                      />
                    ) : (
                      <Sparkles className="w-6 h-6 text-slate-600" />
                    )}
                  </div>

                  <div className="min-w-0">
                    <h4 className="text-base sm:text-lg font-black text-slate-100 group-hover:text-amber-300 truncate">
                      {item.name}
                    </h4>
                    <div className="flex items-center gap-2.5 text-xs sm:text-sm text-slate-400 mt-0.5">
                      <span className="text-slate-300 font-semibold">{item.category}</span>
                      <span>•</span>
                      <span>{item.type}</span>
                      {item.masteryReq > 0 && (
                        <>
                          <span>•</span>
                          <span className="text-amber-400 font-mono font-bold">MR {item.masteryReq}</span>
                        </>
                      )}
                    </div>
                  </div>
                </div>

                {/* Wiki Button */}
                <a
                  href={item.wikiUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 px-4 py-2 rounded-xl bg-amber-500/15 hover:bg-amber-500/30 text-amber-300 text-xs sm:text-sm font-bold border border-amber-500/40 flex-shrink-0 transition-all shadow-md"
                >
                  <span>wiki.warframe.com</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <div className="p-4 bg-[#0a0e1a] border-t border-slate-800 text-xs sm:text-sm text-slate-400 flex items-center justify-between">
          <span>Showing {filteredItems.length} items</span>
          <span className="font-mono text-xs text-amber-400 font-bold">wiki.warframe.com</span>
        </div>

      </div>

    </div>
  );
}
