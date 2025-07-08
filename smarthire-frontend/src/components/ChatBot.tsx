'use client'

import { useState } from 'react'
import { Card } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { motion } from 'framer-motion'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export default function InterviewChatBot() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [interviewStarted, setInterviewStarted] = useState(false)
  const [loading, setLoading] = useState(false)

  const [token, setToken] = useState<string | null>(null)

const sendMessage = async () => {
  if (!input.trim() || !token) return

  const newMessage: Message = { role: 'user', content: input }
  const updatedMessages = [...messages, newMessage]

  setMessages(updatedMessages)
  setInput('')
  setLoading(true)

  try {
    const res = await fetch('http://localhost:5000/interview_chat/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ token, message:input }),
})

    const data = await res.json()

    if (data.reply) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: data.reply },
        data.question ? { role: 'assistant', content: `👉 ${data.question}` } : null,
      ].filter(Boolean) as Message[])
    } else {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: data.message || '✅ Interview complete.' },
      ])
    }
  } catch (error) {
    setMessages((prev) => [
      ...prev,
      { role: 'assistant', content: '⚠️ Failed to get response. Please try again.' },
    ])
  } finally {
    setLoading(false)
  }}


  const handleStart = async () => {
  try {
    const candidateId = 1 // Replace with actual logged-in candidate ID

    const res = await fetch('http://localhost:5000/interview_chat/start_session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ candidate_id: candidateId }),
    })

    const data = await res.json()
    setToken(data.token)

    setInterviewStarted(true)
    setMessages([
      {
        role: 'assistant',
        content: '👋 Welcome to SmartHireAI. Let’s begin your interview. Please introduce yourself.',
      },
    ])
  } catch (error) {
    alert("Failed to start interview session.")
  }
}


  const handleEnd = () => {
    setMessages((prev) => [
      ...prev,
      {
        role: 'assistant',
        content: '✅ Thank you! Your interview is complete. Results will be shared shortly.',
      },
    ])
    setInterviewStarted(false)
  }

  return (
    <Card className="p-6 max-w-4xl mx-auto mt-10 shadow-xl rounded-2xl border border-blue-200 bg-gradient-to-br from-white to-blue-50">
      <h2 className="text-2xl font-bold mb-6 text-blue-700 text-center">
        SmartHireAI Interview Chat
      </h2>

      <div className="h-[400px] overflow-y-auto space-y-3 mb-4 bg-white p-4 border rounded-lg shadow-inner">
        {messages.map((msg, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: msg.role === 'user' ? 50 : -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3 }}
            className={`w-fit max-w-[80%] px-4 py-2 rounded-md text-sm ${
              msg.role === 'user'
                ? 'ml-auto bg-blue-100 text-blue-900'
                : 'mr-auto bg-green-100 text-green-900'
            }`}
          >
            <strong>{msg.role === 'user' ? 'You' : 'SmartHireAI'}:</strong>{' '}
            <span className="whitespace-pre-wrap">{msg.content}</span>
          </motion.div>
        ))}
      </div>

      {interviewStarted ? (
        <div className="flex gap-2 items-center">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your answer..."
            className="flex-1"
            disabled={loading}
          />
          <Button onClick={sendMessage} disabled={loading}>
            {loading ? 'Sending...' : 'Send'}
          </Button>
          <Button variant="outline" onClick={handleEnd} disabled={loading}>
            End
          </Button>
        </div>
      ) : (
        <div className="flex justify-center">
          <Button size="lg" onClick={handleStart}>
            🎯 Start Interview
          </Button>
        </div>
      )}
    </Card>
  )
}
