export default function NumberGuessGame() {
  const React = require('react');
  const { useState, useEffect } = React;
  const { motion, AnimatePresence } = require('framer-motion');
  const { RefreshCw, Trophy, Hash, Sparkles } = require('lucide-react');

  const generateNumber = () => Math.floor(Math.random() * 100) + 1;

  const [target, setTarget] = useState(generateNumber());
  const [guess, setGuess] = useState('');
  const [message, setMessage] = useState('輸入 1 ~ 100 的數字開始挑戰');
  const [attempts, setAttempts] = useState(0);
  const [history, setHistory] = useState([]);
  const [won, setWon] = useState(false);
  const [bestScore, setBestScore] = useState(null);

  useEffect(() => {
    const saved = localStorage.getItem('bestScore');
    if (saved) setBestScore(Number(saved));
  }, []);

  const handleGuess = () => {
    const num = Number(guess);

    if (!num || num < 1 || num > 100) {
      setMessage('請輸入有效數字（1~100）');
      return;
    }

    const newAttempts = attempts + 1;
    setAttempts(newAttempts);
    setHistory([{ value: num }, ...history]);

    if (num === target) {
      setWon(true);
      setMessage(`恭喜答對！答案就是 ${target}`);

      if (!bestScore || newAttempts < bestScore) {
        setBestScore(newAttempts);
        localStorage.setItem('bestScore', newAttempts.toString());
      }
    } else if (num < target) {
      setMessage('太小了，再大一點 ↑');
    } else {
      setMessage('太大了，再小一點 ↓');
    }

    setGuess('');
  };

  const resetGame = () => {
    setTarget(generateNumber());
    setGuess('');
    setMessage('新的遊戲開始！');
    setAttempts(0);
    setHistory([]);
    setWon(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-900 flex items-center justify-center p-6 text-white overflow-hidden relative">
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-10 left-10 w-72 h-72 bg-cyan-500 rounded-full blur-3xl" />
        <div className="absolute bottom-10 right-10 w-80 h-80 bg-purple-500 rounded-full blur-3xl" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="relative backdrop-blur-xl bg-white/10 border border-white/15 rounded-3xl shadow-2xl w-full max-w-lg p-8"
      >
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-black tracking-tight flex items-center gap-3">
              <Sparkles className="text-cyan-400" />
              猜數字
            </h1>
            <p className="text-slate-300 mt-2">挑戰你的直覺與運氣</p>
          </div>

          <button
            onClick={resetGame}
            className="bg-white/10 hover:bg-white/20 transition p-3 rounded-2xl border border-white/10"
          >
            <RefreshCw size={20} />
          </button>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-black/20 rounded-2xl p-4 border border-white/10">
            <div className="text-slate-400 text-sm mb-1">嘗試次數</div>
            <div className="text-3xl font-bold flex items-center gap-2">
              <Hash className="text-cyan-400" />
              {attempts}
            </div>
          </div>

          <div className="bg-black/20 rounded-2xl p-4 border border-white/10">
            <div className="text-slate-400 text-sm mb-1">最佳紀錄</div>
            <div className="text-3xl font-bold flex items-center gap-2">
              <Trophy className="text-yellow-400" />
              {bestScore || '--'}
            </div>
          </div>
        </div>

        <motion.div
          key={message}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-cyan-500/20 to-purple-500/20 border border-cyan-400/20 rounded-2xl p-5 text-center mb-6"
        >
          <p className="text-lg font-medium">{message}</p>
        </motion.div>

        {!won && (
          <div className="flex gap-3 mb-8">
            <input
              type="number"
              value={guess}
              onChange={(e) => setGuess(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleGuess()}
              placeholder="輸入數字"
              className="flex-1 bg-white/10 border border-white/15 rounded-2xl px-5 py-4 outline-none focus:ring-2 focus:ring-cyan-400 text-lg"
            />

            <button
              onClick={handleGuess}
              className="px-6 py-4 rounded-2xl bg-gradient-to-r from-cyan-500 to-blue-600 font-bold hover:scale-105 active:scale-95 transition"
            >
              猜！
            </button>
          </div>
        )}

        <div>
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-semibold">猜測紀錄</h2>
            <span className="text-sm text-slate-400">
              最近 {history.length} 次
            </span>
          </div>

          <div className="flex flex-wrap gap-3 min-h-[60px]">
            <AnimatePresence>
              {history.map((item, index) => (
                <motion.div
                  key={`${item.value}-${index}`}
                  initial={{ opacity: 0, scale: 0.7, y: 10 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  className="px-4 py-2 rounded-xl bg-white/10 border border-white/10 backdrop-blur-md font-semibold"
                >
                  {item.value}
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>

        {won && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            className="mt-8 text-center bg-gradient-to-r from-emerald-500/20 to-cyan-500/20 border border-emerald-400/20 rounded-3xl p-6"
          >
            <div className="text-5xl mb-3">🎉</div>
            <h3 className="text-2xl font-black mb-2">你贏了！</h3>
            <p className="text-slate-300 mb-5">
              你總共用了 {attempts} 次猜中答案
            </p>

            <button
              onClick={resetGame}
              className="px-6 py-3 rounded-2xl bg-white text-slate-900 font-bold hover:scale-105 active:scale-95 transition"
            >
              再玩一次
            </button>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}