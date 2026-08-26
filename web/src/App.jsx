import React, { useState, useEffect, useMemo, useCallback } from 'react';
import Header from './components/Header';
import LoadoutSection from './components/LoadoutSection';
import WikiSearchModal from './components/WikiSearchModal';
import edaData from './data/eda_data.json';
import { 
  playRollSound, 
  playClickSound 
} from './utils/audio';
import { CheckCircle } from 'lucide-react';

function sampleRandom(array, count) {
  const shuffled = [...array].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
}

export default function App() {
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [isRolling, setIsRolling] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [toast, setToast] = useState(null);

  // Loadout state: 3 of each category
  const [loadout, setLoadout] = useState({
    warframes: [],
    primaries: [],
    secondaries: [],
    melees: []
  });

  // Flattened all items for Wiki Search
  const allItems = useMemo(() => {
    return [
      ...(edaData.warframes || []),
      ...(edaData.primary || []),
      ...(edaData.secondary || []),
      ...(edaData.melee || [])
    ];
  }, []);

  const showToast = useCallback((msg) => {
    setToast(msg);
    setTimeout(() => setToast(null), 3000);
  }, []);

  // Initial 3-of-each EDA Roll
  const generateFullRoll = useCallback(() => {
    setLoadout({
      warframes: sampleRandom(edaData.warframes, 3),
      primaries: sampleRandom(edaData.primary, 3),
      secondaries: sampleRandom(edaData.secondary, 3),
      melees: sampleRandom(edaData.melee, 3)
    });
  }, []);

  useEffect(() => {
    generateFullRoll();
  }, [generateFullRoll]);

  // Reroll all equipment
  const handleRerollAll = () => {
    if (soundEnabled) playRollSound();
    setIsRolling(true);

    setTimeout(() => {
      setLoadout({
        warframes: sampleRandom(edaData.warframes, 3),
        primaries: sampleRandom(edaData.primary, 3),
        secondaries: sampleRandom(edaData.secondary, 3),
        melees: sampleRandom(edaData.melee, 3)
      });
      setIsRolling(false);
    }, 200);
  };

  // Reroll single category
  const handleRerollCategory = (catKey) => {
    if (soundEnabled) playRollSound();
    const source = catKey === 'warframes' ? edaData.warframes :
                   catKey === 'primaries' ? edaData.primary :
                   catKey === 'secondaries' ? edaData.secondary : edaData.melee;
    
    setLoadout(prev => ({
      ...prev,
      [catKey]: sampleRandom(source, 3)
    }));
  };

  // Export loadout to Markdown / Discord
  const handleExportMarkdown = () => {
    if (soundEnabled) playClickSound();
    const lines = [
      "🏆 **WARFRAME EDA / ETA LOADOUT PARAMETERS**",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "✨ **WARFRAME CHOICES (3)**"
    ];
    loadout.warframes.forEach((w) => {
      lines.push(`• [${w.name}](${w.wikiUrl}) (MR${w.masteryReq})`);
    });

    lines.push("\n🎯 **PRIMARY WEAPON CHOICES (3)**");
    loadout.primaries.forEach((p) => {
      lines.push(`• [${p.name}](${p.wikiUrl}) - ${p.type} (MR${p.masteryReq})`);
    });

    lines.push("\n🔫 **SECONDARY WEAPON CHOICES (3)**");
    loadout.secondaries.forEach((s) => {
      lines.push(`• [${s.name}](${s.wikiUrl}) - ${s.type} (MR${s.masteryReq})`);
    });

    lines.push("\n⚔️ **MELEE WEAPON CHOICES (3)**");
    loadout.melees.forEach((m) => {
      lines.push(`• [${m.name}](${m.wikiUrl}) - ${m.type} (MR${m.masteryReq})`);
    });

    lines.push("\n🔗 *Generated via Warframe EDA Generator • Official Wiki: wiki.warframe.com*");

    const text = lines.join("\n");
    navigator.clipboard.writeText(text);
    showToast("Loadout copied to clipboard with wiki.warframe.com links!");
  };

  return (
    <div className="min-h-screen flex flex-col justify-between">
      
      {/* Toast Notification */}
      {toast && (
        <div className="fixed bottom-8 right-8 z-50 bg-amber-500 text-slate-950 font-black px-5 py-3 rounded-2xl shadow-2xl flex items-center gap-2.5 border-2 border-amber-300 text-sm animate-in slide-in-from-bottom-5">
          <CheckCircle className="w-5 h-5" />
          <span>{toast}</span>
        </div>
      )}

      {/* Navigation Header */}
      <Header 
        onRerollAll={handleRerollAll}
        onOpenSearch={() => setIsSearchOpen(true)}
        onExportMarkdown={handleExportMarkdown}
        soundEnabled={soundEnabled}
        setSoundEnabled={setSoundEnabled}
        isRolling={isRolling}
      />

      {/* Main Content Area (Spacious 2X Scale) */}
      <main className="max-w-[1750px] mx-auto px-6 sm:px-8 py-8 w-full flex-1">
        <LoadoutSection 
          loadout={loadout}
          onRerollCategory={handleRerollCategory}
        />
      </main>

      {/* Official Wiki Search Modal */}
      <WikiSearchModal 
        isOpen={isSearchOpen}
        onClose={() => setIsSearchOpen(false)}
        allItems={allItems}
      />

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-[#070a14] py-8 text-center text-sm text-slate-400">
        <div className="max-w-[1750px] mx-auto px-6 sm:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="flex items-center gap-1.5">
            <span>Powered by official Warframe data &</span>
            <a 
              href="https://wiki.warframe.com" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-amber-400 font-bold hover:underline flex items-center gap-1"
            >
              <span>wiki.warframe.com</span>
            </a>
          </p>
          <p className="text-slate-500 font-medium">
            3 Warframes • 3 Primaries • 3 Secondaries • 3 Melees
          </p>
        </div>
      </footer>

    </div>
  );
}
