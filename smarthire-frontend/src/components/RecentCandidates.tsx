'use client'

import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

interface Candidate {
  id: number
  name: string
  total_score: number
}

export default function RecentCandidates({ refreshInterviews }: { refreshInterviews: () => void }) {
  const [candidates, setCandidates] = useState<Candidate[]>([])
  const [scoreFilter, setScoreFilter] = useState(0)
  const [sentIds, setSentIds] = useState<number[]>([])

  useEffect(() => {
    fetch('http://localhost:5000/recent_candidates')
      .then(res => res.json())
      .then(data => setCandidates(data))
  }, [])

  const handleSend = async (id: number) => {
    const res = await fetch('http://localhost:5000/send_invitation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ candidate_id: id })
    })

    if (res.ok) {
      alert('Interview scheduled and email sent!')
      setSentIds(prev => [...prev, id]) // remove from filter section
      refreshInterviews()
    } else {
      const err = await res.json()
      alert(`Failed: ${err.error}`)
    }
  }

  const filteredCandidates = candidates.filter(
    c => c.total_score >= scoreFilter && !sentIds.includes(c.id)
  )

  const selectedCandidates = candidates.filter(c => sentIds.includes(c.id))

  return (
    <div className="mt-10 p-6 bg-white border rounded-xl shadow-lg">
      <h2 className="text-xl font-semibold mb-4">Recent Candidates</h2>

      {/* ✅ Filter by Score */}
      <div className="mb-4 flex items-center gap-2">
        <label>Filter (score out of 100) greater than:</label>
        <Input
          type="number"
          value={scoreFilter.toString()}
          onChange={(e) => {
            const value = e.target.value
            const numeric = value.replace(/^0+(?!$)/, '') // remove leading zeros
            setScoreFilter(numeric === '' ? 0 : parseInt(numeric))
          }}
          className="max-w-[100px]"
          placeholder="Score"
        />
      </div>

      {/* ✅ Candidates Table */}
      <table className="w-full text-left">
        <thead>
          <tr className="border-b font-semibold">
            <th>Name</th>
            <th>Score</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {filteredCandidates.map(c => (
            <tr key={c.id} className="border-t">
              <td>{c.name}</td>
              <td>{c.total_score}</td>
              <td>
                <Button onClick={() => handleSend(c.id)}>Send</Button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {filteredCandidates.length === 0 && (
        <p className="text-gray-500 mt-4">No candidates matching the score filter.</p>
      )}

      {/* ✅ Selected for Interview Section */}
      <div className="mt-10">
        <h3 className="text-lg font-bold mb-2">Selected for Interview</h3>
        <ul className="list-disc pl-5 text-sm">
          {selectedCandidates.map(c => (
            <li key={c.id}>{c.name} - Score: {c.total_score}</li>
          ))}
        </ul>
      </div>
    </div>
  )
}
