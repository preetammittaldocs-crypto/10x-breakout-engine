# 10x-breakout-engine
Share market
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KathaKids Neuro-Acoustic Portal - Pain Management Suite</title>
    <!-- Premium Tailwind UI Engine -->
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <style>
        @keyframes pulse-slow {
            0%, 100% { opacity: 0.3; transform: scale(1); }
            50% { opacity: 0.8; transform: scale(1.05); }
        }
        .glow-effect { animation: pulse-slow 4s infinite ease-in-out; }
    </style>
</head>
<body class="bg-[#0b0c10] text-[#c5c6c7] font-sans min-h-screen flex flex-col justify-between selection:bg-[#45f3ff] selection:text-black">

    <!-- Top Navigation Header -->
    <header class="border-b border-[#1f2833] bg-[#1f2833]/30 backdrop-blur-md px-8 py-4 flex justify-between items-center">
        <div class="flex items-center space-x-3">
            <div class="w-3 h-3 rounded-full bg-[#45f3ff] shadow-[0_0_10px_#45f3ff]"></div>
            <h1 class="text-xl font-bold tracking-wide text-white uppercase">KathaKids <span class="text-[#45f3ff] font-light">Neuro-Portal</span></h1>
        </div>
        <div class="bg-[#0b0c10] px-4 py-1.5 rounded-full border border-[#1f2833] text-xs font-mono text-[#45f3ff]">
            SYSTEM STATUS: OPERATIONAL
        </div>
    </header>

    <!-- Main Portal Dashboard Workspace -->
    <main class="max-w-5xl w-full mx-auto p-6 grid grid-cols-1 md:grid-cols-3 gap-6 my-auto">
        
        <!-- Left Panel: Diagnostic & Patient Parameters Configuration -->
        <section class="bg-[#1f2833]/50 border border-[#1f2833] p-6 rounded-2xl flex flex-col justify-between space-y-6 shadow-xl">
            <div>
                <h2 class="text-lg font-semibold text-white mb-2">Diagnostic Profile</h2>
                <p class="text-xs text-[#86c232] mb-4">Select condition topology to configure acoustic matrices.</p>
                
                <div class="space-y-4">
                    <div>
                        <label class="block text-xs uppercase font-mono tracking-wider mb-2 text-gray-400">Target Pathology</label>
                        <select id="painType" class="w-full bg-[#0b0c10] border border-[#1f2833] rounded-xl px-4 py-3 text-white focus:outline-none focus:border-[#45f3ff] transition-all cursor-pointer">
                            <option value="internal">Neuromuscular / Internal (Dystonia, Spasms)</option>
                            <option value="external">Somatic / External Tissue Pain (Acute/Structural)</option>
                        </select>
                    </div>

                    <div class="bg-[#0b0c10]/60 p-4 rounded-xl border border-[#1f2833]/60">
                        <h3 class="text-xs uppercase font-mono text-gray-400 mb-2">Clinical Neuro-Insights</h3>
                        <p id="pathologyInsight" class="text-xs leading-relaxed text-gray-300">
                            Internal neuromuscular spasms require down-regulating hyperactive motor neurons by mapping acoustic signals to the central nervous system's deep relaxation pathways.
                        </p>
                    </div>
                </div>
            </div>

            <!-- Session Controls Trigger Section -->
            <div class="space-y-3">
                <button id="sessionBtn" class="w-full bg-[#45f3ff] hover:bg-[#39d2dd] text-[#0b0c10] font-bold py-4 px-6 rounded-xl shadow-[0_0_20px_rgba(69,243,255,0.2)] hover:shadow-[0_0_25px_rgba(69,243,255,0.4)] transition-all cursor-pointer flex justify-center items-center space-x-2 text-md">
                    <span id="btnIcon">▶</span> <span id="btnText">Initialize Neuro-Sequence</span>
                </button>
                <p class="text-[10px] text-center text-gray-500 italic">Stereo headphones required for correct bilateral phase separation.</p>
            </div>
        </section>

        <!-- Right Panel: Real-Time Dynamic Healing Telemetry Matrix -->
        <section class="md:col-span-2 bg-[#1f2833]/30 border border-[#1f2833] rounded-2xl p-6 flex flex-col justify-between space-y-6 shadow-xl relative overflow-hidden">
            <div class="absolute -top-24 -right-24 w-48 h-48 bg-[#45f3ff]/5 rounded-full blur-3xl glow-effect"></div>
            
            <!-- Real-time Status and Parameters Grid Display -->
            <div class="flex justify-between items-start">
                <div>
                    <span class="text-xs uppercase font-mono tracking-widest text-[#45f3ff]">Acoustic Healing Stream</span>
                    <h2 id="activePhaseTitle" class="text-2xl font-bold text-white mt-1">System Standby</h2>
                </div>
                <div class="text-right">
                    <span class="text-xs uppercase font-mono text-gray-400">Session Timer</span>
                    <div id="timerDisplay" class="text-2xl font-mono font-bold text-white tracking-widest mt-1">30:00</div>
                </div>
            </div>

            <!-- Live Multi-Phase Timeline Track Visualization -->
            <div class="grid grid-cols-3 gap-2 relative z-10">
                <div id="phaseCard1" class="border border-[#1f2833] bg-[#0b0c10]/40 p-3 rounded-xl transition-all duration-500">
                    <div class="text-[10px] font-mono text-gray-500 uppercase">Phase 1 (0-5m)</div>
                    <div class="text-xs font-semibold text-gray-300 mt-1">Gate Control</div>
                </div>
                <div id="phaseCard2" class="border border-[#1f2833] bg-[#0b0c10]/40 p-3 rounded-xl transition-all duration-500">
                    <div class="text-[10px] font-mono text-gray-500 uppercase">Phase 2 (5-20m)</div>
                    <div class="text-xs font-semibold text-gray-300 mt-1">Neural Release</div>
                </div>
                <div id="phaseCard3" class="border border-[#1f2833] bg-[#0b0c10]/40 p-3 rounded-xl transition-all duration-500">
                    <div class="text-[10px] font-mono text-gray-500 uppercase">Phase 3 (20-30m)</div>
                    <div class="text-xs font-semibold text-gray-300 mt-1">Somatic Sync</div>
                </div>
            </div>

            <!-- Real-time Oscillating Waveform Visualization Canvas -->
            <div class="relative bg-[#0b0c10] border border-[#1f2833] h-40 rounded-xl overflow-hidden flex items-center justify-center">
                <canvas id="waveCanvas" class="w-full h-full absolute inset-0 opacity-80"></canvas>
                <div id="canvasPlaceholder" class="text-xs font-mono tracking-wider text-gray-600 uppercase z-10">Audio Engine Offline</div>
            </div>

            <!-- Real-time Metric Readout Strip Layout -->
            <div class="grid grid-cols-3 gap-4 border-t border-[#1f2833] pt-4 font-mono text-xs">
                <div>
                    <span class="block text-gray-500 uppercase text-[10px]">Carrier Target</span>
                    <span id="metricCarrier" class="text-sm font-bold text-white">-- Hz</span>
                </div>
                <div>
                    <span class="block text-gray-500 uppercase text-[10px]">Binaural Offset</span>
                    <span id="metricBinaural" class="text-sm font-bold text-[#45f3ff]">-- Hz</span>
                </div>
                <div>
                    <span class="block text-gray-500 uppercase text-[10px]">Output Ceiling</span>
                    <span id="metricDecibels" class="text-sm font-bold text-[#86c232]">-- dB</span>
                </div>
            </div>
        </section>
    </main>

    <!-- Interactive System Footer Context Notice -->
    <footer class="border-t border-[#1f2833] bg-[#0b0c10] px-8 py-4 text-center text-[11px] text-gray-600 font-mono tracking-wide">
        CLINICAL PLATFORM SPECIFICATION V1.0.4 • POWERED BY NATIVE WEB AUDIO OS ENGINE
    </footer>

    <!-- Native Web Audio Engine Core Application Logic Script Code -->
    <script>
        // System variables & State parameters Configuration
        let audioCtx = null;
        let oscL = null;
        let oscR = null;
        let gainL = null;
        let gainR = null;
        let merger = null;
        let masterGain = null;
        let isRunning = false;
        let currentPhase = 1;
        let timeRemaining = 1800; // 30 Minutes in seconds
        let timerInterval = null;
        let animationFrameId = null;

        // UI Element Selectors Initialization
        const sessionBtn = document.getElementById('sessionBtn');
        const btnIcon = document.getElementById('btnIcon');
        const btnText = document.getElementById('btnText');
        const painTypeSelect = document.getElementById('painType');
        const pathologyInsight = document.getElementById('pathologyInsight');
        const timerDisplay = document.getElementById('timerDisplay');
        const canvasPlaceholder = document.getElementById('canvasPlaceholder');
        const waveCanvas = document.getElementById('waveCanvas');
        const canvasCtx = waveCanvas.getContext('2d');
        
        // Metric Telemetry Display Fields Reference
        const metricCarrier = document.getElementById('metricCarrier');
        const metricBinaural = document.getElementById('metricBinaural');
        const metricDecibels = document.getElementById('metricDecibels');
        const activePhaseTitle = document.getElementById('activePhaseTitle');

        // Pathology Select Event Listener Block
        painTypeSelect.addEventListener('change', (e) => {
            if(e.target.value === 'internal') {
                pathologyInsight.innerText = "Internal neuromuscular spasms require down-regulating hyperactive motor neurons by mapping acoustic signals to the central nervous system's deep relaxation pathways.";
            } else {
                pathologyInsight.innerText = "Somatic and tissue pain requires higher frequency neural gate interruption, effectively overriding standard pain transmission nodes along the spinal nerve track.";
            }
            if(isRunning) updateAudioParameters();
        });

        // Main Session Control Initialization Trigger
        sessionBtn.addEventListener('click', () => {
            if (!isRunning) {
                startAudioEngine();
            } else {
                stopAudioEngine();
            }
        });

        // Native Audio Core Synthesis Implementation Strategy
        function startAudioEngine() {
            // Instantiate Audio Context Object safely inside browser tab container environment
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            
            // Generate standard multi-channel nodal matrix connections
            oscL = audioCtx.createOscillator();
            oscR = audioCtx.createOscillator();
            gainL = audioCtx.createGain();
            gainR = audioCtx.createGain();
            merger = audioCtx.createChannelMerger(2);
            masterGain = audioCtx.createGain();

            // Link discrete left and right oscillation paths into the systemic stereo channel mixer merge nodes
            oscL.connect(gainL);
            oscR.connect(gainR);
            gainL.connect(merger, 0, 0); // Route to Left Speaker channel path
            gainR.connect(merger, 0, 1); // Route to Right Speaker channel path
            
            merger.connect(masterGain);
            masterGain.connect(audioCtx.destination);

            // Set system control variable flag properties
            isRunning = true;
            btnIcon.innerText = "■";
            btnText.innerText = "Terminate Neuro-Sequence";
            canvasPlaceholder.classList.add('hidden');

            // Fire initial telemetry updates and begin calculation loops
            updateAudioParameters();
            oscL.start();
            oscR.start();
            
            startTimerLoop();
            drawWaveformAnimation();
        }

        // Dynamic Frequency Mapping & Parameters Matrix Calculator Engine
        function updateAudioParameters() {
            if(!isRunning) return;

            const isInternal = painTypeSelect.value === 'internal';
            let carrier = 432;
            let offset = 0;
            let volume = 0.5;
            let displayPhaseText = "";

            // Evaluate specific active temporal window layer blocks
            if (timeRemaining > 1500) { // Phase 1: First 5 minutes execution window
                currentPhase = 1;
                carrier = isInternal ? 741 : 880; 
                offset = 40; // 40Hz High Gamma Gate-Interruption wave mechanism
                volume = 0.4;
                displayPhaseText = "Phase 1: Gate-Control Overwrite";
                highlightPhaseCard(1);
            } else if (timeRemaining > 300) { // Phase 2: Middle 5-20 minute therapeutic window
                currentPhase = 2;
                carrier = isInternal ? 174 : 285; // 174Hz specialized neuro-relaxation node
                offset = 4.5; // 4.5Hz Deep Theta Neuromuscular Uncoupling wave
                volume = 0.6;
                displayPhaseText = "Phase 2: Neuromuscular Release";
                highlightPhaseCard(2);
            } else { // Phase 3: Final 20-30 minute stabilization window
                currentPhase = 3;
                carrier = 432; 
                offset = 7.83; // Schumann Resonance Alpha alignment ground phase
                volume = 0.3;
                displayPhaseText = "Phase 3: Somatic Endorphin Integration";
                highlightPhaseCard(3);
            }

            // Target audio processor node parameters smoothly to prevent clicks/pops
            const now = audioCtx.currentTime;
            oscL.frequency.setValueAtTime(carrier, now);
            oscR.frequency.setValueAtTime(carrier + offset, now);
            
            // Set dynamic decibel outputs ceiling controls
            masterGain.gain.setValueAtTime(volume, now);

            // Render updated telemetry readout strings directly onto view elements
            metricCarrier.innerText = `${carrier} Hz`;
            metricBinaural.innerText = `+${offset} Hz (Gamma/Theta)`;
            metricDecibels.innerText = isInternal ? "50-55 dB" : "60 dB Max";
            activePhaseTitle.innerText = displayPhaseText;
        }

        // Timer interface loop tracking countdown seconds remaining
        function startTimerLoop() {
            timerInterval = setInterval(() => {
                if(timeRemaining > 0) {
                    timeRemaining--;
                    // Update timer text layout display panel element
                    let mins = Math.floor(timeRemaining / 60).toString().padStart(2, '0');
                    let secs = (timeRemaining % 60).toString().padStart(2, '0');
                    timerDisplay.innerText = `${mins}:${secs}`;
                    
                    // Periodically execute dynamic parameter sweeps as time progresses
                    if(timeRemaining % 5 === 0) updateAudioParameters();
                } else {
                    stopAudioEngine();
                }
            }, 1000);
        }

        // Highlight the current phase card visually
        function highlightPhaseCard(phaseNum) {
            [1, 2, 3].forEach(num => {
                const card = document.getElementById(`phaseCard${num}`);
                if(num === phaseNum) {
                    card.className = "border border-[#45f3ff] bg-[#45f3ff]/10 p-3 rounded-xl shadow-[0_0_15px_rgba(69,243,255,0.1)] transition-all duration-500";
                } else {
                    card.className = "border border-[#1f2833] bg-[#0b0c10]/40 p-3 rounded-xl transition-all duration-500 opacity-40";
                }
            });
        }

        // Live Canvas visualization script plotting continuous sine outputs
        function drawWaveformAnimation() {
            if(!isRunning) return;
            
            animationFrameId = requestAnimationFrame(drawWaveformAnimation);
            
            // Reset canvas pixel grid space boundary parameters
            waveCanvas.width = waveCanvas.parentElement.clientWidth;
            waveCanvas.height = waveCanvas.parentElement.clientHeight;
            
            canvasCtx.clearRect(0, 0, waveCanvas.width, waveCanvas.height);
            canvasCtx.lineWidth = 2;
            canvasCtx.strokeStyle = currentPhase === 1 ? '#45f3ff' : currentPhase === 2 ? '#86c232' : '#ff007f';
            canvasCtx.beginPath();

            const width = waveCanvas.width;
            const height = waveCanvas.height;
            const sliceWidth = width / 100;
            let x = 0;

            // Generate synthetic oscillatory visual parameters mapped dynamically to current active frequency phase speeds
            let frequencyModifier = currentPhase === 1 ? 0.15 : currentPhase === 2 ? 0.04 : 0.08;
            let timeScale = performance.now() * frequencyModifier;

            for (let i = 0; i < 100; i++) {
                let v = Math.sin((i + timeScale) * 0.3) * (height * 0.25);
                let y = height / 2 + v;

                if (i === 0) {
                    canvasCtx.moveTo(x, y);
                } else {
                    canvasCtx.lineTo(x, y);
                }
                x += sliceWidth;
            }

            canvasCtx.lineTo(width, height / 2);
            canvasCtx.stroke();
        }

        // System shutdown sequence resetting hardware oscillators and parameters safely
        function stopAudioEngine() {
            isRunning = false;
            clearInterval(timerInterval);
            cancelAnimationFrameId = cancelAnimationFrame(animationFrameId);

            if(oscL) { oscL.stop(); oscL.disconnect(); }
            if(oscR) { oscR.stop(); oscR.disconnect(); }
            if(audioCtx) audioCtx.close();

            // Tear down UI dashboard elements to initial offline baseline settings
            btnIcon.innerText = "▶";
            btnText.innerText = "Initialize Neuro-Sequence";
            canvasPlaceholder.classList.remove('hidden');
            activePhaseTitle.innerText = "System Standby";
            timerDisplay.innerText = "30:00";
            timeRemaining = 1800;
            
            metricCarrier.innerText = "-- Hz";
            metricBinaural.innerText = "-- Hz";
            metricDecibels.innerText = "-- dB";
            
            canvasCtx.clearRect(0, 0, waveCanvas.width, waveCanvas.height);
            
            [1, 2, 3].forEach(num => {
                document.getElementById(`phaseCard${num}`).className = "border border-[#1f2833] bg-[#0b0c10]/40 p-3 rounded-xl transition-all duration-500";
            });
        }
    </script>
</body>
</html>
