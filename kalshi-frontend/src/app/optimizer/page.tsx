"use client"

import React, { useEffect, useState, useRef } from 'react'
import gsap from 'gsap'
import SplitType from 'split-type'
import '../globals.css'

const hardcodedBets: Record<string, any[]> = {
    climate: [
      {
        question: "Will LA hit 80°F today?",
        options: [
          { range: "80° or above", percent: 64 },
          { range: "below 80°", percent: 36 },
        ],
        timeLeft: "13h 59m 05s",
        totalVolume: "$3,251,000",
      },
      {
        question: "Will a Category 4+ hurricane make US landfall this year?",
        options: [
          { range: "Yes", percent: 47 },
          { range: "No", percent: 53 },
        ],
        timeLeft: "29d 03h 17m",
        totalVolume: "$2,413,905",
      },
      {
        question: "Will global CO₂ exceed 420ppm by Dec 31?",
        options: [
          { range: "Yes", percent: 71 },
          { range: "No", percent: 29 },
        ],
        timeLeft: "195d 21h 59m",
        totalVolume: "$1,091,784",
      },
      {
        question: "Will Arctic sea ice reach record low in September?",
        options: [
          { range: "Yes", percent: 39 },
          { range: "No", percent: 61 },
        ],
        timeLeft: "75d 13h 11m",
        totalVolume: "$4,008,332",
      },
      {
        question: "Will US wildfire acreage exceed 5M acres this season?",
        options: [
          { range: "Over 5M", percent: 56 },
          { range: "Under 5M", percent: 44 },
        ],
        timeLeft: "40d 16h 48m",
        totalVolume: "$1,869,120",
      },
    ],
  
    finance: [
      {
        question: "Will the S&P 500 close higher today?",
        options: [
          { range: "Yes", percent: 58 },
          { range: "No", percent: 42 },
        ],
        timeLeft: "5h 12m 33s",
        totalVolume: "$10,592,134",
      },
      {
        question: "Will the Fed raise rates at next FOMC meeting?",
        options: [
          { range: "Raise", percent: 21 },
          { range: "Hold", percent: 79 },
        ],
        timeLeft: "12d 04h 09m",
        totalVolume: "$7,184,620",
      },
      {
        question: "Will Bitcoin exceed $70,000 this month?",
        options: [
          { range: "Yes", percent: 33 },
          { range: "No", percent: 67 },
        ],
        timeLeft: "13d 18h 52m",
        totalVolume: "$8,541,290",
      },
      {
        question: "Will US jobless claims fall below 200k next week?",
        options: [
          { range: "Yes", percent: 44 },
          { range: "No", percent: 56 },
        ],
        timeLeft: "6d 14h 21m",
        totalVolume: "$2,370,130",
      },
      {
        question: "Will crude oil exceed $100/barrel before Aug 1?",
        options: [
          { range: "Yes", percent: 40 },
          { range: "No", percent: 60 },
        ],
        timeLeft: "43d 11h 37m",
        totalVolume: "$5,132,894",
      },
    ],
  
    politics: [
      {
        question: "Will Biden win the 2024 presidential election?",
        options: [
          { range: "Yes", percent: 48 },
          { range: "No", percent: 52 },
        ],
        timeLeft: "141d 02h 10m",
        totalVolume: "$12,000,800",
      },
      {
        question: "Will the US House flip to Democratic control?",
        options: [
          { range: "Yes", percent: 55 },
          { range: "No", percent: 45 },
        ],
        timeLeft: "140d 21h 48m",
        totalVolume: "$6,749,300",
      },
      {
        question: "Will a woman be elected VP in 2024?",
        options: [
          { range: "Yes", percent: 62 },
          { range: "No", percent: 38 },
        ],
        timeLeft: "140d 02h 32m",
        totalVolume: "$3,440,920",
      },
      {
        question: "Will any third-party candidate get 5%+ of the vote?",
        options: [
          { range: "Yes", percent: 17 },
          { range: "No", percent: 83 },
        ],
        timeLeft: "139d 22h 11m",
        totalVolume: "$1,982,580",
      },
      {
        question: "Will Trump participate in the first 2024 debate?",
        options: [
          { range: "Yes", percent: 67 },
          { range: "No", percent: 33 },
        ],
        timeLeft: "82d 17h 03m",
        totalVolume: "$4,298,155",
      },
    ],
  };

export default function OptimizerPage() {
  const [showCards, setShowCards] = useState(false)
  const [buttonSlid, setButtonSlid] = useState(false)
  const [query, setQuery] = useState("")
  const [matchedBets, setMatchedBets] = useState<any[]>([])

  const buttonRef = useRef<HTMLButtonElement | null>(null)
  const cardsRef = useRef<HTMLDivElement>(null)
  const contentRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const splitH1 = new SplitType('.optimizer-h1', { types: 'words,chars' })
    const splitH2 = new SplitType('.optimizer-h2', { types: 'words,chars' })
    const splitP = new SplitType('.optimizer-p', { types: 'words,chars' })
    const splitFooter = new SplitType('.optimizer-footer-p', { types: 'words,chars' })

    gsap.from(splitH2.chars, { opacity: 0, y: 20, duration: 0.5, stagger: { amount: 0.2 }, ease: 'power2.out' })
    gsap.from(splitH1.chars, { opacity: 0, y: 20, duration: 0.5, stagger: { amount: 0.2 }, delay: 0.2, ease: 'power2.out' })
    gsap.from(splitP.chars, { opacity: 0, y: 20, duration: 0.5, stagger: { amount: 0.2 }, delay: 0.4, ease: 'power2.out' })
    gsap.from(splitFooter.chars, { opacity: 0, y: 20, duration: 0.5, stagger: { amount: 0.2 }, delay: 0.6, ease: 'power2.out' })

    return () => {
      splitH1.revert()
      splitH2.revert()
      splitP.revert()
      splitFooter.revert()
    }
  }, [])

  useEffect(() => {
    if (showCards && buttonRef.current && contentRef.current && cardsRef.current) {
      const tl = gsap.timeline()

      tl.to(contentRef.current, {
        y: -30,
        duration: 0.6,
        ease: 'power2.inOut',
      })

      tl.to(buttonRef.current, {
        y: 60,
        duration: 0.6,
        ease: 'power2.inOut',
      }, '<')

      tl.fromTo(
        cardsRef.current.children,
        { opacity: 0, y: 30 },
        {
          opacity: 1,
          y: 0,
          duration: 0.6,
          stagger: 0.1,
          ease: 'power2.out',
        },
        '+=0.2'
      )
    }
  }, [showCards])

  const handleAnalyze = () => {
    const key = query.trim().toLowerCase()
    if (hardcodedBets[key]) {
      setMatchedBets(hardcodedBets[key])
      setShowCards(true)
      setButtonSlid(true)
    } else {
      setMatchedBets([])
      setShowCards(false)
    }
  }
  

  return (
    <div className="optimizer">
      <nav className="optimizer-nav">
        <h2 className="optimizer-h2">
          K<span className="white-text lowercase">ai</span>RO
        </h2>
      </nav>

      <main className="optimizer-main">
        <div className="optimizer-stack">

          <section className="optimizer-content" ref={contentRef}>
            <h1 className="optimizer-h1">Real-Time Bet Optimization</h1>
            <p className="optimizer-p">Enter a Kalshi question or choose from trending markets below.</p>
            <input
              type="text"
              placeholder="Choose between {Finance, Politics, Climate}"
              className="optimizer-input"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </section>

          {showCards && (
            <div className="optimizer-cards" ref={cardsRef}>
              {matchedBets.map((bet, i) => (
                <div className="optimizer-card" key={i}>
                <p className="card-question">{bet.question}</p>
              
                <div className="card-options">
                  {bet.options.map((opt: { range: string; percent: number }, j: number) => (
                    <div key={j} className="card-option-row">
                      <span className="range">{opt.range}</span>
                      <span className="percent">{opt.percent}%</span>
                      <span className="yes-no">Yes / No</span>
                    </div>
                  ))}
                </div>
              
                <div className="card-footer">
                  <span className="volume">{bet.totalVolume}</span>
                  <span className="card-time">{bet.timeLeft}</span>
                </div>
              </div>
           ))}
            </div>
          )}

          <div
            style={{
              position: 'relative',
              height: buttonSlid ? 120 : 'auto',
              transition: 'height 0.7s cubic-bezier(0.23, 1, 0.32, 1)',
            }}
          >
            <button
              className="optimizer-button"
              ref={buttonRef}
              onClick={handleAnalyze}
              style={{ zIndex: 10 }}
            >
              Analyze
            </button>
          </div>

        </div>
      </main>

      <footer className="optimizer-footer">
        <p className="optimizer-footer-p">powered by KAIro AI · live Kalshi feed</p>
      </footer>
    </div>
  )
}
