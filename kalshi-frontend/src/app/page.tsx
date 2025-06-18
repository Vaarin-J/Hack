// src/app/page.tsx
'use client'

import React, { useEffect } from 'react'
import useLandingAnimations from './useLandingAnimations.js'
import './globals.css'
import Link from 'next/link'



export default function LandingPage() {
  useLandingAnimations()

  return (
    <div className="hero">
      <div className="progress-bar">
        <p>loading</p>
        <p>/<span id="counter">0</span></p>
      </div>

      <div className="video-container">
        <video autoPlay loop muted playsInline>
          <source src="/brain.mp4" type="video/mp4" />
        </video>
      </div>

      <nav>
        <p>&#9679;</p>
        <p>&#9679;</p>
      </nav>

      <footer>
        <p>contact</p>
        <p>betting</p>
        <p>rankings</p>
        <p>news</p>
      </footer>

      <div className="header">
        <h1><span>Outsmart the Crowd.</span></h1>
        <h1><span> - KAIro - </span></h1>
        <h1><span>on Kalshi.</span></h1>

        <Link href="/optimizer" className="cta-button">Find Your Bets</Link>
      </div>



      <div className="logo">
        <div className="char"><h1>C</h1></div>
        <div className="char anim-out"><h1>l</h1></div>
        <div className="char anim-out"><h1>a</h1></div>
        <div className="char anim-out"><h1>s</h1></div>
        <div className="char anim-out"><h1>h</h1></div>
        <div className="char anim-out"><h1>o</h1></div>
        <div className="char anim-out"><h1>n</h1></div>
        <div className="char anim-in"><h1>.</h1></div>
      </div>
    </div>
  )
}