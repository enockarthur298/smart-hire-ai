  'use client'

  interface ResumeResultCardProps {
    data: {
      score: number
      parsed: {
        name: string
        skills: string[]
        experience: number
        education: string
        cgpa: string
      }
    }
  }

  export default function ResumeResultCard({ data }: ResumeResultCardProps) {
    const { score, parsed } = data

    return (
      <div className="mt-6 p-6 bg-white border rounded-xl shadow-lg max-w-md space-y-4">
        <h2 className="text-2xl font-bold text-blue-700">
          {parsed.name}
        </h2>

        <div className="text-gray-700 space-y-2">
          <p><span className="font-semibold">Score:</span> {score}/100</p>
          <p><span className="font-semibold">Skills:</span> {parsed.skills?.join(', ') || 'N/A'}</p>
          <p><span className="font-semibold">Experience:</span> {parsed.experience} year(s)</p>
          <p><span className="font-semibold">CGPA:</span> {parsed.cgpa}</p>
          <p><span className="font-semibold">Education:</span> {parsed.education}</p>
        </div>
      </div>
    )
  }
