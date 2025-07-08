'use client'

import ResumeUploadForm from '@/components/ResumeUploadForm'
import { useState } from 'react'
import ResumeResultCard from '@/components/ResumeResultCard'





export default function DashboardPage() {
  const [result, setResult] = useState(null)

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">SmartHireAI - HR Dashboard</h1>
      <ResumeUploadForm setResult={setResult} />
      {result && <ResumeResultCard data={result} />}
    </div>
  )
}
