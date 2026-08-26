import React from 'react';
import { 
  Shield, 
  Crosshair, 
  Flame, 
  Sword, 
  RefreshCw, 
  ExternalLink, 
  Sparkles
} from 'lucide-react';

const CATEGORY_META = {
  warframes: {
    title: 'Warframe',
    icon: Shield,
    color: 'text-amber-400',
    borderColor: 'border-amber-500/40',
    accent: 'amber'
  },
  primaries: {
    title: 'Primary Weapon',
    icon: Crosshair,
    color: 'text-cyan-400',
    borderColor: 'border-cyan-500/40',
    accent: 'cyan'
  },
  secondaries: {
    title: 'Secondary Weapon',
    icon: Flame,
    color: 'text-emerald-400',
    borderColor: 'border-emerald-500/40',
    accent: 'emerald'
  },
  melees: {
    title: 'Melee Weapon',
    icon: Sword,
    color: 'text-purple-400',
    borderColor: 'border-purple-500/40',
    accent: 'purple'
  }
};

function EquipmentCard({ item }) {
  if (!item) return null;

  return (
    <div 
      className="relative group rounded-2xl border transition-all duration-300 flex flex-col justify-between overflow-hidden bg-[#0d1222]/90 border-slate-800/90 hover:border-amber-500/50 hover:bg-[#11172e] shadow-xl"
    >
      {/* Card Showcase Area */}
      <div className="p-6 sm:p-7 flex flex-col items-center text-center flex-1">
        
        {/* Large Item Image Thumbnail */}
        <div className="relative mb-5 flex items-center justify-center">
          <div className="w-32 h-32 sm:w-36 sm:h-36 rounded-2xl bg-[#070a14] border-2 border-slate-800/90 group-hover:border-amber-500/50 p-2.5 flex items-center justify-center shadow-inner group-hover:shadow-[0_0_25px_rgba(212,175,55,0.2)] transition-all overflow-hidden">
            {item.imageUrl ? (
              <img 
                src={item.imageUrl} 
                alt={item.name}
                className="w-full h-full object-contain filter drop-shadow-lg group-hover:scale-110 transition-transform duration-300"
                onError={(e) => {
                  e.target.style.display = 'none';
                }}
              />
            ) : (
              <Sparkles className="w-12 h-12 text-slate-600" />
            )}
          </div>
        </div>

        {/* Item Title & Classification */}
        <div className="w-full">
          <h4 className="text-xl sm:text-2xl font-black text-slate-100 group-hover:text-amber-300 transition-colors truncate tracking-wide" title={item.name}>
            {item.name}
          </h4>

          <div className="flex items-center justify-center gap-2.5 mt-1.5 text-sm text-slate-300 font-semibold">
            <span>{item.type}</span>
            {item.masteryReq > 0 && (
              <>
                <span className="text-slate-600">•</span>
                <span className="px-2 py-0.5 text-xs font-mono font-bold bg-slate-800/90 text-amber-400 border border-amber-500/30 rounded">
                  MR {item.masteryReq}
                </span>
              </>
            )}
          </div>

          {item.description && (
            <p className="text-xs sm:text-sm text-slate-400 line-clamp-3 mt-3 italic font-sans leading-relaxed px-1">
              "{item.description}"
            </p>
          )}
        </div>

      </div>

      {/* Card Footer with Direct Wiki Button */}
      <div className="p-4 bg-slate-950/60 border-t border-slate-800/70 flex items-center justify-center">
        <a
          href={item.wikiUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="w-full flex items-center justify-center gap-2 py-2.5 px-4 text-xs sm:text-sm font-bold text-amber-300 hover:text-amber-200 bg-amber-950/40 hover:bg-amber-900/60 border border-amber-500/40 hover:border-amber-400 rounded-xl transition-all shadow-md hover:shadow-amber-500/20"
          title="Open article on wiki.warframe.com"
        >
          <span>wiki.warframe.com</span>
          <ExternalLink className="w-4 h-4" />
        </a>
      </div>
    </div>
  );
}

export default function LoadoutSection({
  loadout,
  onRerollCategory
}) {
  const categories = [
    { key: 'warframes', ...CATEGORY_META.warframes },
    { key: 'primaries', ...CATEGORY_META.primaries },
    { key: 'secondaries', ...CATEGORY_META.secondaries },
    { key: 'melees', ...CATEGORY_META.melees }
  ];

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
        {categories.map((cat) => {
          const Icon = cat.icon;
          const items = loadout[cat.key] || [];

          return (
            <div 
              key={cat.key}
              className={`orokin-card rounded-2xl p-6 sm:p-7 border ${cat.borderColor} flex flex-col justify-between shadow-2xl`}
            >
              {/* Category Header */}
              <div className="flex items-center justify-between mb-6 pb-4 border-b border-slate-800">
                <div className="flex items-center gap-3.5">
                  <div className={`p-2.5 rounded-xl bg-slate-900 border border-slate-700 shadow-md ${cat.color}`}>
                    <Icon className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-cinzel text-xl sm:text-2xl font-black tracking-wider text-slate-100 uppercase">
                      {cat.title}
                    </h3>
                    <span className="text-xs sm:text-sm text-slate-400 font-medium">
                      3 Equipment Choices
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => onRerollCategory(cat.key)}
                  className="flex items-center gap-2 px-4 py-2 text-xs sm:text-sm font-bold rounded-xl bg-slate-800/90 hover:bg-slate-700 text-slate-200 hover:text-white border border-slate-600 transition-all shadow-md"
                  title={`Reroll all 3 ${cat.title} choices`}
                >
                  <RefreshCw className="w-4 h-4" />
                  <span>Reroll Category</span>
                </button>
              </div>

              {/* 3 Choices Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
                {items.map((item, idx) => (
                  <EquipmentCard
                    key={`${cat.key}-${idx}-${item.name}`}
                    item={item}
                  />
                ))}
              </div>

            </div>
          );
        })}
      </div>
    </div>
  );
}
