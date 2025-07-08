'use client'

import { useState } from 'react'
import InterviewSchedule from '@/components/InterviewSchedule'
import RecentCandidates from '@/components/RecentCandidates'

export default function InterviewPage() {
  const [refreshKey, setRefreshKey] = useState(0)

  const refreshInterviews = () => {
    setRefreshKey(prev => prev + 1)
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Interview Schedule</h1>
      
      {/* ✅ ONLY ONCE */}
      <InterviewSchedule key={refreshKey} />
      
      <RecentCandidates refreshInterviews={refreshInterviews} />
    </div>
  )
}
