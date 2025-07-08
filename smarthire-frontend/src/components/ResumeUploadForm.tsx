'use client'

import { useState } from 'react'
import { UploadCloud, Loader2 } from 'lucide-react'

interface ResumeUploadFormProps {
  setResult: (data: any) => void
}

export default function ResumeUploadForm({ setResult }: ResumeUploadFormProps) {
  const [loading, setLoading] = useState(false)

  const handleUpload = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const form = e.currentTarget
    const fileInput = form.resume as HTMLInputElement

    if (!fileInput.files?.length) return

    const formData = new FormData()
    formData.append('resume', fileInput.files[0])

    setLoading(true)

    try {
      const res = await fetch('http://localhost:5000/upload_resume', {
        method: 'POST',
        body: formData,
      })

      const data = await res.json()
      setResult(data)
    } catch (err) {
      console.error('Upload failed:', err)
      alert('Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form
      onSubmit={handleUpload}
      className="w-full max-w-md p-6 bg-white rounded-2xl shadow-lg border border-gray-200 space-y-4"
    >
      <div>
        <label className="block mb-1 font-medium text-gray-700">Upload Resume</label>
        <input
          type="file"
          name="resume"
          accept=".pdf,.txt"
          required
          className="block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4
                     file:rounded-lg file:border-0 file:text-sm file:font-semibold
                     file:bg-blue-100 file:text-blue-700 hover:file:bg-blue-200"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="flex items-center justify-center gap-2 w-full bg-blue-600 hover:bg-blue-700
                   text-white font-semibold py-2 px-4 rounded-lg transition duration-200 disabled:opacity-50"
      >
        {loading ? (
          <>
            <Loader2 className="animate-spin w-4 h-4" />
            Analyzing...
          </>
        ) : (
          <>
            <UploadCloud className="w-4 h-4" />
            Upload & Analyze
          </>
        )}
      </button>
    </form>
  )
}
