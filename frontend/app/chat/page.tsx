"use client"

import { useState, ChangeEvent, KeyboardEvent } from "react";
import Image from "next/image";
import ReactMarkdown from 'react-markdown';
import ava from "../../assets/ava.svg";
import submit from "../../assets/submit.svg";
import button_return from "../../assets/return.svg";
import rewrite from "../../assets/rewrite.svg";
import loading from "../../assets/loading.gif";
import Link from "next/link";

interface ChatMessage {
  user: string;
  bot: string | null;
}

interface MarkdownComponentProps {
  children: React.ReactNode;
}

const Screen = () => {
  const [inputValue, setInputValue] = useState<string>("");
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleInputChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
    const textarea = event.target;
    textarea.style.height = "40px";
    textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`;
    setInputValue(textarea.value);
  };

  const handleSubmit = async () => {
    if (inputValue.trim()) {
      const userMessage = inputValue;
      setInputValue("");
      
      setChatHistory(prev => [...prev, { user: userMessage, bot: null }]);
      setIsLoading(true);

      try {
        const response = await fetch(`http://127.0.0.1:8000/ask?query=${encodeURIComponent(userMessage)}`, {
          method: "GET",
          headers: {
            'Accept': 'application/json',
          },
        });
        
        const { response: botResponse } = await response.json();
        
        setChatHistory(prev => prev.map((msg, idx) => 
          idx === prev.length - 1 ? { ...msg, bot: botResponse } : msg
        ));
      } catch (error) {
        console.error("Error fetching response:", error);
        setChatHistory(prev => prev.map((msg, idx) => 
          idx === prev.length - 1 ? { ...msg, bot: "Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại." } : msg
        ));
      } finally {
        setIsLoading(false);
        const textarea = document.querySelector(".input") as HTMLTextAreaElement;
        if (textarea) {
          textarea.style.height = "40px";
        }
      }
    }
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && !event.shiftKey && inputValue.trim()) {
      event.preventDefault();
      handleSubmit();
    }
  };

  const handleRewrite = (index: number) => {
    setInputValue(chatHistory[index].user);
    setChatHistory(chatHistory.slice(0, index));
  };

  // Loading animation component
  const LoadingDots = () => (
    <div className="flex items-center gap-1">
      <span className="animate-bounce delay-0">.</span>
      <span className="animate-bounce delay-100">.</span>
      <span className="animate-bounce delay-200">.</span>
    </div>
  );

  // Custom components for markdown rendering
  const markdownComponents = {
    p: ({ children }: MarkdownComponentProps) => <p className="mb-2">{children}</p>,
    strong: ({ children }: MarkdownComponentProps) => <strong className="font-bold">{children}</strong>,
    em: ({ children }: MarkdownComponentProps) => <em className="italic">{children}</em>,
    ul: ({ children }: MarkdownComponentProps) => <ul className="list-disc ml-4 mb-2">{children}</ul>,
    ol: ({ children }: MarkdownComponentProps) => <ol className="list-decimal ml-4 mb-2">{children}</ol>,
    li: ({ children }: MarkdownComponentProps) => <li className="mb-1">{children}</li>,
  };

  return (
    <div className="relative w-full h-screen bg-gradient-to-b from-[#B2F7F8] to-[#B1EAFE]">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 flex items-center justify-center h-16 bg-white/30 backdrop-blur-sm shadow-sm">
        <Link className="absolute left-2 transform hover:scale-110 transition-transform" href={"/"}>
          <button>
            <Image src={button_return} alt="Return" width={32} height={32} />
          </button>
        </Link>

        <div className="flex items-center gap-2">
          <Image
            src={ava}
            alt="Ava Đậu Đậu"
            width={40}
            height={40}
            className="transform hover:scale-110 transition-transform"
          />
          <p className="font-['Baloo_Da'] text-2xl text-[#2C5A87]">Đậu Đậu</p>
        </div>
      </header>

      {/* Chat Container */}
      <main className="pt-20 pb-24 px-4 h-full overflow-y-auto">
        <div className="max-w-4xl mx-auto flex flex-col gap-4">
          {chatHistory.map((entry, index) => (
            <div key={index} className="flex flex-col gap-4">
              {/* User Message */}
              <div className="flex justify-end items-start gap-2">
                <button
                  className="opacity-50 hover:opacity-100 transition-opacity"
                  onClick={() => handleRewrite(index)}
                >
                  <Image src={rewrite} alt="Rewrite" width={20} height={20} />
                </button>
                <div className="bg-[#2C5A87] text-white rounded-2xl px-4 py-3 max-w-[80%]">
                  {entry.user}
                </div>
              </div>
              
              {/* Bot Message */}
              {entry.bot === null && isLoading && index === chatHistory.length - 1 ? (
              <div className="flex items-start gap-2">
                <Image
                  src={ava}
                  alt="Avatar"
                  width={32}
                  height={32}
                  className="mt-1"
                />
                <div className="bg-white rounded-2xl px-4 py-3 max-w-[80%] text-[#0D2849]">
                  <div className="flex items-center h-6 text-2xl font-bold">
                    <Image src={loading} alt="Loading" width={56} height={96} />
                  </div>
                </div>
              </div>
            ) : (
              entry.bot !== null && (
                <div className="flex items-start gap-2">
                  <Image
                    src={ava}
                    alt="Avatar"
                    width={32}
                    height={32}
                    className="mt-1"
                  />
                  <div className="bg-white rounded-2xl px-4 py-3 max-w-[80%] text-[#0D2849]">
                    <ReactMarkdown 
                      components={markdownComponents}
                      className="prose prose-sm max-w-none"
                    >
                      {entry.bot.replace(/\*\*/g, '**').replace(/\n/g, '  \n')}
                    </ReactMarkdown>
                  </div>
                </div>
              )
            )}
            </div>
          ))}
        </div>
      </main>

      {/* Input Area */}
      <footer className="fixed bottom-0 left-0 right-0 bg-white/30 backdrop-blur-sm p-4">
        <div className="max-w-4xl mx-auto flex items-end gap-2">
          <textarea
            className="input flex-1 bg-white rounded-2xl px-4 py-3 font-['Baloo_Da_2'] outline-none border-none resize-none overflow-y-auto min-h-[40px] max-h-[120px]"
            placeholder="Nhập thông tin cần tìm hiểu..."
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
          />
          <button 
            className="bg-transparent border-none transform scale-60 hover:scale-75 transition-transform" 
            onClick={handleSubmit}
            disabled={!inputValue.trim() || isLoading}
          >
            <Image src={submit} alt="Submit" width={32} height={32} />
          </button>
        </div>
      </footer>
    </div>
  );
};

export default Screen;