'use client';

import { useState } from 'react';

export default function QuestionsPage() {
  const [jd, setJd] = useState('');
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/generate-questions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ job_description: jd }),
      });
      if (!res.ok) throw new Error(`API error: ${res.status}`);
      const data = await res.json();
      setQuestions(data.questions);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">Generate Interview Questions</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          rows={6}
          className="w-full border rounded p-2"
          placeholder="Paste your job description here..."
          value={jd}
          onChange={(e) => setJd(e.target.value)}
        />
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
          disabled={loading || !jd.trim()}
        >
          {loading ? 'Generating…' : 'Generate Questions'}
        </button>
      </form>

      {error && (
        <p className="mt-4 text-red-600">Error: {error}</p>
      )}

      {questions.length > 0 && (
        <div className="mt-6">
          <h2 className="text-2xl font-semibold mb-2">Questions</h2>
          <ul className="list-decimal list-inside space-y-1">
            {questions.map((q, i) => (
              <li key={i}>{q}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
