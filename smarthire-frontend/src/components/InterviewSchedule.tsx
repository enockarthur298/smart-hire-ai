'use client'
import { useEffect, useState } from 'react'


interface Interview {
  id: number
  candidate_name: string
  interview_date: string
  start_time: string
  end_time: string
  status: string
}

export default function InterviewSchedule() {
  const [interviews, setInterviews] = useState<Interview[] | null>(null)

  useEffect(() => {
    const fetchInterviews = async () => {
      try {
        const res = await fetch('http://localhost:5000/interviews')
        if (!res.ok) throw new Error('Failed to fetch interviews')
        const data = await res.json()
        setInterviews(data) // your backend returns a flat array
      } catch (err) {
        console.error('Fetch error:', err)
        setInterviews([]) // fallback to empty array to avoid crash
      }
    }

    fetchInterviews()
  }, [])

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Interview Schedule</h1>

      {!interviews ? (
        <p>Loading...</p>
      ) : interviews.length === 0 ? (
        <p>No interviews scheduled yet.</p>
      ) : (
        <ul className="space-y-4">
          {interviews.map((i) => (
            <li key={i.id} className="border rounded-lg p-4 shadow-sm bg-white">
              <p><strong>Candidate:</strong> {i.candidate_name}</p>
              <p><strong>Date:</strong> {i.interview_date}</p>
              <p><strong>Time:</strong> {i.start_time} - {i.end_time}</p>
              <p><strong>Status:</strong> {i.status}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
