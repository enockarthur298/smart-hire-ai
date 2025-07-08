// app/chat/page.tsx
'use client'
import InterviewChatBot from '@/components/ChatBot'

export default function ChatPage() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Interview Chat</h1>
      <InterviewChatBot />
    </div>
  )
}
