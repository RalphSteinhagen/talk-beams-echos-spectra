---
title: Beams, Echoes and Spectra
author: Ralph J. Steinhagen, GSI/FAIR Darmstadt, Darmstadt, Germany
numbering: number
---

# {#title master=title}

:::place
ttl: 0.0357 0.0300 0.6700 0.1500
sub: 0.0357 0.1800 0.6700 0.1300
pano: 0.0200 0.3200 0.9600 0.5947
byline: 0.0357 0.9161 0.6000 0.0650
:::

:::layout
logo: media/gnuradiodays-2026-banner-cutout.webp
:::

:::ttl {notes=off size=480%}
**Beams, Echoes and Spectra**
:::

:::sub {notes=off size=180%}
*From wartime navigation and radar to particle accelerators*<br>*and software-defined radio*
:::

:::byline {size=130% centre}
[**Ralph J. Steinhagen, GSI/FAIR, Darmstadt, Germany**]{colour=#ffff00}
:::

:::pano {notes=off fit}
![the century as one panorama, grey turning to colour from left to right: the Laue pattern, the 1917 sound-ranging headquarters, the Armistice film, Lawrence's cyclotron, a radar operator, LEP's cavities, the Effelsberg dish, a satellite, the Whirlpool galaxy](figures/emblem-montage.webp)
:::

:::notes
- the thesis: different fields keep solving the same problems under different names — the ideas echo, cross over and come back; this talk follows those echoes
- the three words change meaning as we go: beams (navigation, radar, particles), echoes (radar, ideas, history), spectra (carriers, noise, the beam's own)
- the panorama turns from grey to colour, 1912 to today[^ph-panorama]
- bridge: "it starts on paper, in 1865 — with a wave nobody had seen"
:::

# The Birth of RF<br>Maxwell predicts, Hertz measures — a wave becomes an instrument {#hertz master=people}

:::place
mxhead: 0.0357 0.1250 0.3600 0.0600
maxwell: 0.0357 0.1950 0.3600 0.6200
p1: 0.8607 0.0190 0.1143 0.2950
hzhead: 0.4063 0.1250 0.4366 0.0600
engraving: 0.4063 0.1950 0.1875 0.3200
photo: 0.5938 0.1950 0.2500 0.3200
caption: 0.4063 0.5050 0.4366 0.0400
light: 0.4063 0.5500 0.4366 0.1000
useless: 0.4063 0.6550 0.4366 0.0450
quote: 0.4622 0.6950 0.3800 0.1300
marconi: 0.5188 0.8350 0.3244 0.0450
p2: 0.8607 0.3222 0.1143 0.2950
:::

:::mxhead {notes=off size=110%}
**1865: Maxwell predicts RF waves — on paper**[^maxwell]
:::

:::maxwell {notes=off fit}
$$
\begin{gathered}
\begin{aligned}
& \text{\tiny Gauss' law for electricity:} & \nabla \cdot \mathbf{D} &= \rho \\
& \text{\tiny Gauss' law for magnetism:} & \nabla \cdot \mathbf{B} &= 0 \\
& \text{\tiny Faraday's law of induction:} & \nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}}{\partial t} \\
& \text{\tiny Ampère's law:} & \nabla \times \mathbf{H} &= \mathbf{J} + \frac{\partial \mathbf{D}}{\partial t} \\
& \rule{0pt}{1.8em}\text{\tiny material equations:} & &
\end{aligned} \\
\scalebox{0.75}{\displaystyle \mathbf{D} = \varepsilon_0 \mathbf{E} + \mathbf{P} \qquad \mathbf{H} = \frac{1}{\mu_0} \mathbf{B} - \mathbf{M}}
\end{gathered}
$$
:::

:::p1 {notes=off size=40% fit}
![James Clerk Maxwell](media/portraits/maxwell.webp)

[**James Clerk Maxwell**]{size=205%}<br>[1831–1879]{size=205%}
:::

:::step

:::p2 {notes=off size=40% fit}
![Heinrich Hertz](media/hertz-portrait.webp)

[**Heinrich Hertz**]{size=205%}<br>[1857–1894]{size=205%}
:::

:::hzhead {notes=off size=110%}
**1887, Karlsruhe: Hertz makes them — sees sparks across the room**[^hertz]
:::

:::engraving {notes=off fit}
![Hertz's electromagnetism experiments, 1880s: battery, induction coil with its interrupter, spark-gap transmitter, parabolic mirrors, prism and resonator](media/hertz-apparatus-spl.webp)
:::

:::photo {notes=off fit}
![Hertz's original apparatus on the laboratory tables: induction coil, the dipole with its two spheres, receiving loops and a cylindrical reflector](media/hertz-laboratory.webp)
:::

:::caption {notes=off size=caption}
battery, coil, spark gap, mirrors, prism, resonator[^ph-spl] — and the apparatus itself[^ph-hertzlab]
:::

:::light {notes=off}
- measured like light: wavelength, reflection, refraction, polarisation, interference — and **characterised by resonance**
:::

:::step

:::useless {notes=off}
- his conclusion, as the story goes:
:::

:::quote {notes=off size=225%}
"It's of no use whatsoever"
:::

:::marconi {notes=off}
— Marconi and Tesla, ten years later …
:::

[^maxwell]: J. C. Maxwell, "A dynamical theory of the electromagnetic field," *Phil. Trans. R. Soc. Lond.*, vol. 155, pp. 459–512, 1865.
[^hertz]: H. Hertz, *Electric Waves: Being Researches on the Propagation of Electric Action with Finite Velocity Through Space*, transl. D. E. Jones. London: Macmillan, 1893.

:::notes
- the first pair: Maxwell predicts on paper (1865); Hertz makes the wave (1887) and measures it like light — Maxwell never saw the wave, Hertz never saw the use
- the quote, as the story goes [verify: quotation and source] — ten years later Marconi and Tesla make it wireless telegraphy
- the four verbs of every later system are already here: generate · propagate · detect · resonate
- bridge: "twenty-five years later the same wave physics reads a crystal — with X-rays"
:::

# Laue Sees Spots, the Father Measures, the Son Interprets<br>X-rays and crystals, Munich, Leeds and Cambridge, 1912–1915 {#xrays master=people}

:::place
h1: 0.0357 0.1250 0.2063 0.0450
laueimg: 0.0357 0.1700 0.1763 0.3160
laueapp: 0.0357 0.4900 0.1763 0.4030
l1: 0.0357 0.8760 0.2063 0.0560
p1: 0.8607 0.0190 0.1143 0.2850
h2: 0.2544 0.1250 0.2881 0.0450
spectro: 0.2544 0.1700 0.2431 0.4550
measure: 0.2544 0.6089 0.2431 0.2711
c2: 0.2544 0.8700 0.2881 0.0350
p2: 0.8607 0.3080 0.1143 0.2850
h3: 0.5550 0.1250 0.2881 0.0450
schematic: 0.5550 0.1700 0.2881 0.3667
l3: 0.5550 0.5400 0.3000 0.2400
p3: 0.8607 0.5970 0.1143 0.2850
nobel: 0.0357 0.9350 0.8072 0.0550
m1: 0.9538 0.2322 0.0350 0.0622
m2: 0.9538 0.5211 0.0350 0.0622
m3: 0.9538 0.8100 0.0350 0.0622
:::

:::p1 {notes=off size=40% fit}
![Max von Laue](media/portraits/laue.webp)

[**Max von Laue**]{size=205%}<br>[1879–1960]{size=205%}
:::

:::h1 {notes=off size=110%}
**1912: X-Rays through a Crystal**
:::

:::laueimg {notes=off fit}
![a Laue X-ray diffraction photograph from the Braggs' 1915 book](media/laue-pattern-1915.webp)
:::

:::l1 {notes=off size=caption}
Munich[^ph-laueapp]: von Laue sees a regular pattern of spots<br>→ X-rays are waves, a crystal is a grating[^ph-laue]
:::

:::laueapp {notes=off fit}
![the original Laue apparatus of 1912 in the Deutsches Museum: X-ray tube, crystal holder, lead box and plate on a wooden table under an easel](media/laue-apparatus-dm.webp)
:::

:::step

:::p2 {notes=off size=40% fit}
![William Henry Bragg](media/portraits/bragg-wh.webp)

[**William Henry Bragg**]{size=205%}<br>[1862–1942]{size=205%}
:::

:::h2 {notes=off size=110%}
**1913, Leeds: the father measures**
:::

:::spectro {notes=off fit}
![William Henry Bragg's ionisation spectrometer, 1912–13, Royal Institution](media/bragg-spectrometer-rigb.webp)
:::

:::measure {notes=off fit}
![W. H. and W. L. Bragg's 1913 measurement: ionisation against the angle for two faces of rock salt, sharp peaks A, B, C in first and second order](media/bragg-1913-rocksalt.webp)
:::

:::c2 {notes=off size=caption}
ionisation spectrometer[^ph-rigb] and measurement[^bragg1913]
:::

:::step

:::p3 {notes=off size=40% fit}
![William Lawrence Bragg](media/bragg-wl-nobel-1915.webp)

[**William Lawrence Bragg**]{size=205%}<br>[1890–1971]{size=205%}
:::

:::h3 {notes=off size=110%}
**1912, Cambridge: the son interprets**
:::

:::schematic {notes=off fit}
![Bragg's law: two reflections from planes d apart leave in phase when 2d sin θ is a whole number of wavelengths](figures/bragg-law.svg)
:::

:::l3 {notes=off size=125%}
- reflections from **planes of atoms**
- in phase when $n\lambda = 2d\sin\theta$
- **path difference, phase, interference**
:::

:::step

:::nobel {notes=off size=110%}
**1914 & 1915 Nobel Prizes:** making the invisible visible — a crystal lattice read from its echoes — the talk's first **inverse problem**
:::

:::m1 {notes=off fit}
![a Nobel Prize medal](media/nobel-medal.webp)
:::

:::m2 {notes=off fit}
![a Nobel Prize medal](media/nobel-medal.webp)
:::

:::m3 {notes=off fit}
![a Nobel Prize medal](media/nobel-medal.webp)
:::

[^bragg1913]: W. H. Bragg and W. L. Bragg, "The reflection of X-rays by crystals," *Proc. R. Soc. Lond. A*, vol. 88, no. 605, pp. 428–438, 1913.

:::notes
- Laue asks, the father measures, the son interprets (the slide follows the roles; the son's law came first, November 1912)
- Laue's spots: X-rays are waves, a crystal is a grating; the father's spectrometer is a swept, narrowband receiver — a spectrum analyser for X-rays; the son reads planes of atoms, in phase when 2d sin θ = nλ
- click 3: Nobel 1914 and 1915; the son, 25, hears of it at the front
- what the son carries into the war: path difference, phase, interference
- bridge: "three years later the wave is a gun's report at 20 Hz — first, the war"
:::

# 1914–1918: Europe Thrown into Chaos<br>From Flanders to the Somme: remembrance — and an engineering problem {#flanders}

:::place
poppies: 0.0357 0.1670 0.4900 0.6133
bleuet: 0.0007 0.1048 0.0700 0.1244
ranging: 0.5356 0.1670 0.4288 0.6133
text: 0.0357 0.7750 0.9286 0.1200
:::

:::poppies {notes=off fit}
![a field of red poppies before the Thiepval Memorial to the Missing of the Somme, its arch rising above the trees](media/poppies-thiepval.webp)
:::

:::bleuet {notes=off fit}
![the Bleuet de France, the French flower of remembrance](figures/bleuet-de-france.svg)
:::

:::ranging {notes=off fit}
![a German soldier of an artillery sound-ranging unit at a camouflaged listening post with a two-horn listener, June 1917](media/sound-ranging-post-1917.webp)
:::

:::text {notes=off size=130%}
**Two legacies of the same war**: remembering the loss and those who served, so that we can live free and at peace in Europe<br>— and a spark of ideas that are still evolving
:::

:::notes
- 30 seconds, said calmly, then move on:
- "Last Wednesday was the 108th anniversary of the Armistice. In 1914, Europe was thrown into chaos. History doesn't repeat itself, but it often rhymes — and its echoes reach us still. Let us remember all who served and all who died, on every side."
- the poppies are at Thiepval, on the Somme; the same war, some 90 km north: Lawrence Bragg sets up the first British sound-ranging section near Ypres, in Flanders, in late 1915
:::

# A New Type of War: Shelled from out of Sight … Where Is That Gun?<br>sound ranging works on a quiet range and fails at the front {#problem}

:::place
text: 0.0357 0.1250 0.5300 0.1800
text2: 0.0357 0.2550 0.5300 0.2200
moerser: 0.1481 0.4666 0.3250 0.4689
station: 0.6188 0.0579 0.3562 0.5420
circled: 0.6188 0.0579 0.3562 0.5420
clip: 0.6188 0.5800 0.3562 0.2600
clipcap: 0.6188 0.8420 0.3562 0.0600
:::

:::text {notes=off}
- **devastating**: artillery causes most of the casualties — soldiers no longer face each other; they are shelled from kilometres away by guns they never see
- the eye fails (night, fog, hidden flashes), the ear and a stopwatch are too coarse
:::

:::moerser {notes=off size=caption fit}
![a German 21 cm Mörser heavy howitzer of the First World War, preserved in a museum](media/moerser-21cm.webp)

German 21 cm Mörser: 11 km range, fired from behind a hill[^ph-moerser]
:::

:::step

:::text2 {notes=off}
- **the French idea**, 1914: Nordmann and Bull — microphones on a surveyed base, measure the **delays** between them[^costley]
- on a quiet range near Paris: a gun to 40 m; at the front the carbon microphones hear the shell's **supersonic crack**, the bursts, rifles and machine guns — not the gun
:::

:::station {notes=off fit}
![diagram of a sound-ranging base: six microphones on an arc behind the front line, observation posts at both ends, lines to Central](media/sr-base-hinman-1919.webp)
:::

:::clip {notes=off fit}
:::video
src: media/armistice-coda-to-coda.webm
audio: true
autoplay: false
loop: false
:::
:::

:::clipcap {notes=off size=caption}
a sound-ranging base, after J. R. Hinman, 1919[^ph-hinman]; sound ranging film, IWM Q 47886,<br>11:00, 11 November 1918[^iwmq47886] — P for the sonification by Coda to Coda[^coda]
:::

:::step {in=fade}

:::circled {notes=off fit}
![the same diagram with the six microphones circled](media/sr-base-hinman-1919-mics.webp)
:::

[^costley]: R. D. Costley Jr., "Battlefield acoustics in the First World War: artillery location," *Acoustics Today*, vol. 16, no. 2, pp. 31–39, 2020, doi: 10.1121/AT.2020.16.2.31.
[^iwmq47886]: Imperial War Museums, sound-ranging film record of the artillery activity on the American front near the River Moselle, one minute before and after the Armistice, 11 Nov. 1918, American Embassy Collection, catalogue no. Q 47886, IWM Non Commercial Licence. [Online]. Available: https://www.iwm.org.uk/collections/item/object/205281906
[^coda]: Coda to Coda, "IWM – WW1 Armistice Interpretation (Sound Installation)," 1 min, released 6 Nov. 2018, all rights reserved. [Online]. Available: https://codatocoda.bandcamp.com/album/iwm-ww1-armistice-interpretation-sound-installation

:::notes
- said once: we can learn from this past twice — as citizens, so that it never happens again, and as engineers: the problems solved under fire are the ones we still solve
- a new kind of war: guns firing from out of sight; the eye (balloons, flash spotting) fails in fog and at night, the ear and a stopwatch are too coarse — the geometry needs milliseconds
- click 1, the French idea: Nordmann (an astronomer) and Bull (galvanometers from cardiography): time the report at several microphones; November 1914, near Saint-Cloud, a gun located to ~40 m — on a quiet range
- at the front it fails: three sounds per shot, and the microphones answer the shell's crack, the bursts and the rifles; wind and temperature bend the sound
- P on the film: Coda to Coda's interpretation of the Armistice record, ~20 s across 11:00 — careful: "a modern sonification of the 1918 record", never "the actual sound"
- click 2: the circles — six microphones on a 7 km arc
- bridge: "let's try it ourselves — a drum, four microphones, and you"
:::

# Experiment 1: a Drum, Four Microphones — and Shakers<br>Nordmann and Bull's sound-ranging experiment, and why it failed at the front {#exp1}

:::place
live: 0.0357 0.1250 0.9286 0.7250
toolbar: 0.3500 0.8550 0.6143 0.0900
card0: 0.0250 0.5200 0.3325 0.4800
photo: 0.0357 0.5280 0.3150 0.4300
photocap: 0.1306 0.9420 0.2000 0.0400
card1: 0.0250 0.5200 0.3325 0.4800
group: 0.0357 0.5280 0.3150 0.4450
:::

:::gr4
id: exp1
region: live
workflow: workflows/exp1-claps.grc
lifecycle: run-while-visible
toolbar: toolbar
:::

:::card0 {notes=off fit layer=above}
![a piece of the chalkboard over the live region's placeholder pane](figures/chalk-patch-exp1.webp)
:::

:::photo {notes=off fit layer=above}
![an Austro-Hungarian sound-ranging headquarters, 1917: an operator with headphones at the recorder](media/sound-ranging-hq-1917.webp)
:::

:::photocap {notes=off size=caption layer=above}
1917: a sound-ranging headquarter[^ph-sr]
:::

:::step

:::card1 {notes=off fit layer=above}
![a piece of the chalkboard, laid over the headquarters photo](figures/chalk-patch-exp1.webp)
:::

:::group {notes=off size=caption fit layer=above}
![the sound-ranging team round a table, c. 1916: standing Tucker, Atkins, Paris; seated Golt, Lucien Bull, W. L. Bragg and a French officer](media/sr-group-1916-ri.webp)

Tucker, Bull, Bragg, Paris and colleagues, c. 1916[^ph-srgroup]
:::

:::notes
- before the talk: `devtools/four-mics-browser-pairs.sh setup`; `input` on the microphones (simulation as the fallback); once the viewer carries `align: once`, the first clap straight in front of mic 2
- the set-up in one breath: four microphones on a line, 1 m apart — a sound-ranging base in miniature — an audio interface, a laptop, one flow-graph inside the slides
- hit the drum: the hits step down the stacked traces — mic 1 chalk, orange, blue, olive; read one delay aloud (sound covers 34 cm per ms); each delay is a hyperbola, they cross at the drum
- hand out the shakers: the trigger fires on the hiss, the chart loses the drum — "this is the front in 1916: the microphones hear everything except the gun"
- click: the people who solved it together — the French and British sound rangers at one table (Bull seated, bearded; Bragg in the peaked cap; Tucker standing left); 1917: ~25 m, reported within 10 minutes
- 1917 → today: the film became an ADC, the ruler a least-squares fit
- plant the echo: "keep these hyperbolae in mind — they come back in navigation"
- bridge, shakers still going: "how do you hear the gun and not the crack? Tucker lay in a hut with holes in it …"
:::

# Experiment 2: 1916 — Tucker's Microphone<br>then: a hot wire in an ammunition box (Helmholtz resonator); today: a digital band-/low-pass {#lowpass}

:::place
live: 0.0357 0.1250 0.9286 0.7250
toolbar: 0.3500 0.8550 0.6143 0.0900
card: 0.0250 0.5200 0.3325 0.3600
mic: 0.0357 0.5280 0.3150 0.3300
miccap: 0.0357 0.8650 0.3150 0.0700
popup: 0.2500 0.1300 0.4500 0.7700
:::

:::gr4
id: lowpass
region: live
workflow: workflows/exp1b-lowpass.grc
lifecycle: run-while-visible
toolbar: toolbar
:::

:::card {notes=off fit layer=above}
![a piece of the chalkboard over the live region's placeholder pane](figures/chalk-patch-left.webp)
:::

:::mic {notes=off fit layer=above}
![Tucker's first hot-wire microphone: an empty S.A.A. ammunition box, a hot-wire grid across a drilled hole, leads to a galvanometer; the inset shows air pumped in and out through the hole past the wire](figures/tucker-ammo-box.svg)
:::

:::miccap {notes=off size=caption}
Tucker's hot wire, 1916[^ph-tuckermic] — the gun's slow puff cools it, the shell's crack does not — a band-pass in brass[^iwm]
:::

:::step {in=grow}

:::popup {notes=off fit layer=above}
![a Tucker hot-wire microphone in its fitted case: a brass tube resonator with the ebonite holder for the hot-wire grid; engineered: a Tucker hot-wire microphone, National Physical Laboratory](media/tucker-microphone-smg.webp)
:::

[^iwm]: Imperial War Museums, "Sound Ranging Explained." [Online]. Available: https://www.iwm.org.uk/history/first-world-war/western-front/sound-ranging-explained

:::notes
- two people, two kinds of knowledge: Tucker the experimentalist (hot wires), Bragg the wave physicist (phase, interference)
- as Bragg told it (1971): Tucker felt cold air puffing through the holes of his hut each time a heavy gun fired — a wire across the hole of an ammunition box: the shell's crack "hardly made the galvanometer quiver", the gun "gave an enormous kick"
- why: the box is a Helmholtz resonator, a band-pass filter in brass and air, tuned to the gun's 10–25 Hz
- live, shakers still going: drag the band's upper edge down onto the drum — the hiss leaves the traces, the trigger fires on the drum again, the chart finds it again
- the price: the narrower the band, the slower the edges — time resolution against noise, the trade-off that runs through the rest of the talk
- the 1916 fix, relived in software: re-doing it is how it is understood, not just known
- click (after dragging — the pop-up covers the charts): the engineered microphone, a tuned brass resonator
- bridge: "basic science, a real problem, engineering, better instruments — and the same pattern in every field: one problem, many disguises"
:::

# One Problem, Many Disguises<br>basic science → a real problem → engineering → better instruments {#chain}

:::place
chain: 0.0357 0.1150 0.9286 0.2690
questions: 0.0357 0.3900 0.9286 0.2550
braid: 0.0357 0.6550 0.9286 0.3360
:::

:::chain {notes=off fit}
![the recurring chain: excite → propagate → interact → observe → infer → control, and the loop back from control to excite](figures/pipeline.svg)
:::

:::questions {notes=off striped size=90%}
| 1887 Hertz | 1900s radio | 1912 the Braggs | 1915 Bragg, Tucker | 1920s RF acceleration | 1930s navigation | 1935 radar | 1940 SIGINT | 1970s beam diagnostics | today LLRF, feedback |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| *does the wave exist?* | *what did you say?* | *where are the atoms?* | *where is that gun?* | *when do I push?* | *where am I?* | *where are you?* | *what are you doing?* | *what is the beam doing?* | *can I hold it there?* |
:::

:::braid {notes=off fit}
![the braid of four strands up to 1918, the future dimmed: Hertz, Röntgen and Laue by name; sound ranging on the radar strand; Bull's galvanometer film and Tucker's hot wire on the instruments strand](figures/braid-1918.svg)
:::

:::notes
- read the chain once: excite → propagate → interact → observe → infer → control; under each box the same thing in different fields' words — spark, gun, carrier, RF pulse, bunch; coherer, microphone, antenna, pickup, ADC
- read four of the questions, not all ten: where is that gun? · where am I? · where are you? · what is the beam doing? — one chain, many disguises, many vocabularies
- the strip beneath: the braid to 1918 — the first crossing (wave physics into acoustics); the instruments strand still cyan — today these are blocks
- bridge: "Rutherford wanted faster projectiles — one goal, two routes"
:::

# One Big Push, or Many Small Timed Ones? — RF "accelerates" Particles<br>Lord Rutherford wanted faster projectiles — two routes, 1924–1932 {#widero master=people}

:::place
h1: 0.0357 0.1250 0.4625 0.0450
ising: 0.0357 0.1700 0.2169 0.2789
bild1: 0.2575 0.1700 0.2375 0.2789
cap1: 0.0357 0.4450 0.4625 0.0350
cyclo: 0.0357 0.4850 0.2031 0.3244
t1: 0.2500 0.4850 0.2482 0.3000
h2: 0.5125 0.1250 0.3306 0.0450
cascade: 0.5125 0.1700 0.2063 0.5022
t2: 0.5125 0.6750 0.3306 0.1800
waltonline: 0.0357 0.8700 0.8072 0.0500
people: 0.8607 0.0190 0.1143 0.8667
:::

:::h1 {notes=off size=110%}
**many small pushes, in phase — radio**
:::

:::ising {notes=off fit}
![Ising's 1924 drawing: a discharge tube with three cylindrical electrodes fed by spark-gap pulses over lines of different length](media/ising-1924-linac.webp)
:::

:::bild1 {notes=off fit}
![Widerøe's 1928 drawing of the principle: four drift tubes I–IV on one alternating voltage, the ions gain the voltage at every gap](media/wideroe-1928-bild1.webp)
:::

:::cap1 {notes=off size=caption}
Ising's proposal, 1924 · Widerøe's principle, 1928[^ph-wideroe]
:::

:::cyclo {notes=off size=caption fit}
![M. Stanley Livingston and Ernest O. Lawrence in front of the 27-inch cyclotron, Berkeley, 1930s](media/lawrence-cyclotron.webp)

Livingston and Lawrence, the 27-inch cyclotron[^ph-cyclotron]
:::

:::t1 {notes=off}
- 1924 Ising proposes, 1928 Widerøe builds: **RF hands energy to ions**, in phase with their flight[^waloschek]
- 1929 Lawrence reads the diagrams; 1931: **the cyclotron**
- the route to the energy frontier
:::

:::h2 {notes=off size=110%}
**one big push — static**
:::

:::cascade {notes=off size=caption fit}
![a Cockcroft–Walton voltage-multiplier cascade from the Cavendish Laboratory, columns of rectifiers and capacitors under a large electrode, on display in the Science Museum, London](media/cockcroft-walton-cascade-cavendish.webp)

a Cockcroft–Walton cascade, Cavendish
:::

:::t2 {notes=off}
- 14 April 1932, Cockcroft and Walton: **p + Li → 2α** — the first disintegration by artificially accelerated particles, from ~125 kV[^betatron]
- first to the milestone; RF went further — static machines live on as injectors
:::

:::waltonline {notes=off}
Walton had tried Widerøe's route first — the ray-transformer on his own, the drift tube after reading him: both failed.
:::

:::people {notes=off size=40% fit}
![Ernest Rutherford](media/portraits/rutherford.webp)

[**Ernest Rutherford**]{size=205%}<br>[1871–1937]{size=205%}

![Rolf Widerøe](media/portraits/wideroe.webp)

[**Rolf Widerøe**]{size=205%}<br>[1902–1996]{size=205%}

![Ernest Walton](media/portraits/walton.webp)

[**Ernest Walton**]{size=205%}<br>[1903–1995]{size=205%}
:::

[^waloschek]: P. Waloschek, *The Infancy of Particle Accelerators: Life and Work of Rolf Wideröe*. Braunschweig: Vieweg, 1994. [Online]. Available: https://www-library.desy.de/elbook.html

:::notes
- Rutherford wanted energetic projectiles to probe nuclei — and had started in radio himself (his detector of Hertzian waves, 1894); a static voltage is limited by breakdown: one big push, or many small pushes timed by radio?
- the timed route: Ising proposes (1924), Widerøe builds it (1928): RF hands energy to ions, in phase with their flight — radio technology crosses into accelerator physics; Lawrence "skipped the German text and read the diagrams" → the cyclotron (1931)
- the static route: Cockcroft and Walton, 14 April 1932, lithium split at ~125 kV — first to the milestone; RF went further, static machines live on as injectors
- careful: the two routes are a fork, not a crossing
- the footer: Walton had tried Widerøe's route first — both failed; bridge: "the idea that failed twice"
:::

# The Betatron Widerøe Could Have Built<br>an idea from 1922 — lost to isolation and a bare glass wall, made to work by Kerst in 1940 {#betatron}

:::place
fig: 0.0357 0.1250 0.4800 0.3722
text: 0.0357 0.5100 0.4800 0.4000
photo: 0.5500 0.1250 0.3294 0.7300
:::

:::fig {notes=off size=caption fit}
![Widerøe's 1928 drawing of the ray-transformer: an iron core with the main winding W1, the doughnut-shaped tube R between the guide poles Bs, electrons injected at K](media/wideroe-1928-bild11.webp)

Widerøe's ray-transformer, 1928 (Bild 11)[^ph-wideroe]
:::

:::text {notes=off}
- **1922**, a student's notebook: the ray-transformer, its 2:1 rule — an old idea[^waloschek]
- **1926–27**, Aachen: ~1½ turns — charge on the **bare glass wall**, no focusing yet;<br>Rogowski (his PhD advisor): no doctorate "for something that did not function" — he builds the linac instead
- alone, then war: Walton (1928) and Steenbeck (1935) fail or stay secret;<br>[**NOBODY COMPARES NOTES**]{colour=#ffcc00}
- **1940**, Kerst: added a thin, grounded **silver film** inside the glass & a focusing field<br>— voilà: 2.3 MeV, the **betatron**[^betatron]
- 1941: one *Physical Review* reaches occupied Norway — "like a thunderbolt";<br>the word stays: **betatron oscillations**, the tune
:::

:::photo {notes=off size=caption fit}
![a Kerst betatron at the University of Illinois, its large magnet surrounded by apparatus, with Kerst and colleagues at work](media/betatron-kerst-1942.webp)

1942 betatron, Illinois (Electronics, 1942)
:::

[^betatron]: J. D. Cockcroft and E. T. S. Walton, "Disintegration of lithium by swift protons," *Nature*, vol. 129, p. 649, 1932; E. T. S. Walton, "The production of high speed electrons by indirect means," *Proc. Camb. Phil. Soc.*, vol. 25, pp. 469–481, 1929; D. W. Kerst, "The acceleration of electrons by magnetic induction," *Phys. Rev.*, vol. 60, pp. 47–53, 1941; D. W. Kerst and R. Serber, "Electronic orbits in the induction accelerator," *Phys. Rev.*, vol. 60, pp. 53–58, 1941.

:::notes
- the idea is old: 1922, Widerøe's student notebook — electrons accelerated by a changing flux, the beam as a transformer's secondary, the 2:1 condition; Slepian (1922), Breit and Tuve (1927), Walton (1928) and Steenbeck had pieces of it too — none knew of the others: NOBODY COMPARES NOTES
- in Aachen the electrons ran ~1½ turns: charge on the bare glass wall, no orbit theory, a professor who would not give a doctorate for "something that did not function"
- 1940, Kerst: a grounded silver film on the glass, Serber's orbit theory — it works, citing Widerøe and Walton; the beam's wobble is still called "betatron oscillation"
- 1941, occupied Oslo: one smuggled copy of Physical Review — Widerøe in the audience: "like a thunderbolt"
- the speaker's view, said as such: a brief exchange in the late 1920s could have given us these machines a decade earlier; then the war caught Widerøe in between — he built a betatron in Hamburg (1943–45), was not trusted in Germany, was penalised for collaboration in Norway and kept at arm's length abroad — his own account in Waloschek's biography[^waloschek] (also Sørheim 2020)
- careful: wall charging, not "resistive-wall instability"; the coating is Kerst's, not AdA's
- bridge: "back to radio — and again two routes to one goal: how does an aircraft find its way without sight?"
:::

# Transmit the Direction, or Measure the Delays?<br>two routes to the same goal — on approach today, both {#navigation}

:::place
h1: 0.0357 0.1250 0.4543 0.0450
lorenz: 0.0357 0.1700 0.4100 0.2400
lz: 0.0357 0.3950 0.4543 0.0420
ye: 0.0357 0.4550 0.2900 0.2300
sectors: 0.3400 0.4450 0.1500 0.2600
yecap: 0.0357 0.6800 0.4543 0.0800
ils: 0.0357 0.7650 0.2300 0.1500
today: 0.2800 0.7600 0.2250 0.1700
h2: 0.5100 0.0250 0.4543 0.0450
loran: 0.5100 0.0700 0.4543 0.4800
lorcap: 0.6300 0.5300 0.3300 0.0700
quote: 0.5100 0.6100 0.4543 0.1000
t3: 0.5100 0.7150 0.3400 0.1500
wrline: 0.5100 0.8750 0.2700 0.0500
wrlogo: 0.7850 0.8550 0.0600 0.0850
:::

:::h1 {notes=off size=110%}
**transmit the direction**
:::

:::lorenz {notes=off fit}
![the Lorenz beam: two overlapping lobes, dots on one side and dashes on the other, a steady tone on the centre line where they overlap; three aircraft](media/lorenz-beam-dahnielson.svg)
:::

:::lz {notes=off}
Lorenz 1932: fly the equisignal[^ph-lorenz]
:::

:::step

:::ye {notes=off fit}
![USS Belleau Wood, 18 April 1943: the escort carrier with its antennas marked in the photograph, among them YE, the Hayrake homing beacon at the masthead](media/hayrake-ye-belleau-wood-1943.webp)
:::

:::sectors {notes=off fit}
![the YE beacon turns at about 2 rpm and keys a different Morse letter into each 30-degree sector; an aircraft hears its sector's letter and flies the reciprocal home](figures/hayrake-sectors.svg)
:::

:::yecap {notes=off}
YE–ZB "Hayrake", NRL 1937: a Morse letter per 30° sector — home to a moving airfield[^nav]
:::

:::step

:::ils {notes=off fit}
![an ILS localiser antenna array beside a runway: a row of orange dipole masts](media/ils-localizer-eddv.webp)
:::

:::today {notes=off size=90%}
today:
- **ILS** — Instrument Landing System
- **VOR** — VHF Omnidirectional Range
- **TACAN** — Tactical Air Navigation
:::

:::step

:::h2 {notes=off size=110%}
**measure the delays**
:::

:::loran {notes=off fit}
![a LORAN diagram: a pair of transmitting stations on the coast and the hyperbolic lines of position they define over the sea](media/loran-hyperbolic-pattern-1949-stations.webp)
:::

:::lorcap {notes=off}
Gee 1942–43, LORAN (Rad Lab)<br>Decca, OMEGA: the same but phase
:::

:::quote {notes=off}
"similar in principle … with reversal of the direction of travel of the signals" — the Rad Lab's *Loran* volume, 1948, on WWI sound ranging[^nav]
:::

:::t3 {notes=off size=90%}
today:
- **GNSS** — Global Navigation Satellite Systems
- **DME** — Distance Measuring Equipment
- multilateration
:::

:::wrline {notes=off size=90%}
down the line: precision time-keeping → **White Rabbit**
:::

:::wrlogo {notes=off fit}
![the White Rabbit logo](media/white-rabbit-logo.png)
:::

[^nav]: Smithsonian National Air and Space Museum, "Time and Navigation." [Online]. Available: https://timeandnavigation.si.edu/; J. A. Pierce, A. A. McKenzie and R. H. Woodward, Eds., *Loran*, MIT Radiation Laboratory Series, vol. 4. New York: McGraw-Hill, 1948, §1-4, p. 10; L. A. Gebhard, *Evolution of Naval Radio-Electronics and Contributions of the Naval Research Laboratory*, NRL Report 8300, 1979, pp. 272–274.

:::notes
- the fork: guide or locate an aircraft without sight — transmit the direction, or measure the delays; neither was wrong, an airliner on approach today uses both
- direction: Lorenz (1932) — fly the equisignal; click 1, Hayrake (US Navy, 1937): the home airfield moves, a rotating beacon keys a letter into each 30° sector; click 2, today ILS, VOR, TACAN — successors, not descendants
- careful: Hayrake is a parallel route to the same goal, not a counter to Knickebein; the Royal Navy's Type 72 is co-evolution
- click 3, delays: Gee and LORAN (proposed 1940, in service 1942–43) — each time difference a hyperbola, two cross at the aircraft: experiment 1's hyperbolae with the roles reversed — the echo we planted
- the quote: the Rad Lab's own book makes the comparison with WWI sound ranging — a link in the explanation, not a documented line of invention
- today: GNSS — the fit of experiment 1, plus a clock term; and White Rabbit, the accelerators' sub-nanosecond timing, now on the ground beside GNSS
- bridge: "a navigation beam is a transmitter whose receiver may be on the other side's aircraft"
:::

# A Different "Battle of the Beams"<br>electronic warfare grows up — intercept, jam, spoof {#beams master=people}

:::place
map: 0.0357 0.1300 0.4000 0.5110
ov0: 0.0357 0.1300 0.4000 0.5110
ov1: 0.0357 0.1300 0.4000 0.5110
ov2: 0.0357 0.1300 0.4000 0.5110
ov3: 0.0357 0.1300 0.4000 0.5110
mapcap: 0.0357 0.6500 0.4000 0.0400
clock0: 0.4500 0.1300 0.3950 0.5450
clock1: 0.4500 0.1300 0.3950 0.5450
clock2: 0.4500 0.1300 0.3950 0.5450
clock3: 0.4500 0.1300 0.3950 0.5450
close: 0.0357 0.7400 0.8000 0.0800
p1: 0.8607 0.0190 0.1143 0.2950
bbc: 0.8607 0.3350 0.1143 0.2322
ally: 0.8607 0.5700 0.1143 0.2722
allycap: 0.8607 0.8420 0.1143 0.0600
:::

:::map {notes=off fit}
![the Knickebein transmitters in the Low Countries and on the Channel coast, and two beams, from Kleve and from Stollberg, crossing over Derby](media/knickebein-map-dahnielson.svg)
:::

:::ov0 {notes=off fit}
![a bomber rides the Kleve beam towards the crossing over Derby](figures/beams-map-0.svg)
:::

:::mapcap {notes=off size=caption}
Knickebein, 1940: two beams cross over Derby
:::

:::clock0 {notes=off fit}
![June 1940: Knickebein — fly the equisignal, drop at the crossing; found by R. V. Jones's team](figures/race-clock-0.svg)
:::

:::p1 {notes=off size=40% fit}
![Reginald V. Jones](media/portraits/jones-rv.webp)

[**Reginald V. Jones**]{size=205%}<br>[1911–1997]{size=205%}
:::

:::step

:::ov1 {notes=off fit}
![ASPIRIN: a British jammer in the Midlands, and the extra dots it lays on the beam](figures/beams-map-1.svg)
:::

:::clock1 {notes=off fit}
![August to October 1940: ASPIRIN — find the modulation, add the dots; the beam is not bent, it is misread](figures/race-clock-1.svg)
:::

:::step

:::ov2 {notes=off fit}
![X-Gerät: a director beam from the Cherbourg peninsula to Coventry with three timed cross-beams; BROMIDE's jammer near the target](figures/beams-map-2.svg)
:::

:::clock2 {notes=off fit}
![November 1940: X-Gerät receivers filter at 2000 Hz; BROMIDE jammed at 1500 Hz, then at 2000](figures/race-clock-2.svg)
:::

:::step

:::ov3 {notes=off fit}
![Y-Gerät: one beam and two-way ranging to the aircraft; DOMINO answers from Alexandra Palace](figures/beams-map-3.svg)
:::

:::clock3 {notes=off fit}
![February 1941: Y-Gerät ranges by an echo; DOMINO, on the BBC's television transmitter, answers phase-shifted](figures/race-clock-3.svg)
:::

:::bbc {notes=off fit}
![the BBC's tower at Alexandra Palace, London: brick corner towers framing white bay windows, the television mast on top, 2015](media/alexandra-palace-bbc-tower-2015.webp)
:::

:::ally {notes=off fit}
![the BBC's television mast on the tower of Alexandra Palace, silhouetted against a grey sky, 1975](media/alexandra-palace-mast-1975.webp)
:::

:::allycap {notes=off size=caption}
DOMINO's transmitter: Alexandra Palace[^ph-allybbc][^ph-ally]
:::

:::step

:::close {notes=off}
radio navigation, **not radar** — the first fully fought electronic war[^jones]
:::

[^jones]: R. V. Jones, *Most Secret War: British Scientific Intelligence 1939–1945*. London: Hamish Hamilton, 1978.

:::notes
- the map and the race clock, four clicks: German guidance in green, the British counter in red — move and counter-move in weeks, not years
- June 1940, Knickebein: a Lorenz-type beam from Kleve, a second from Stollberg crossing it over the target — a civil blind-landing aid turned bombing aid (T); R. V. Jones finds it (the Anson flight of 21 June 1940)
- Aug–Oct 1940, ASPIRIN: listen, identify the modulation, add dots so the pilot hears a confused course; say "not bent — misread": the indication was falsified, the beam was not bent (the Germans believed it was)
- Nov 1940, X-Gerät / BROMIDE: receivers filtered at 2000 Hz; the first jammers modulated at 1500 Hz and missed the filter; the right frequency came from the He 111 that landed at West Bay on 6 November; corrected after Coventry (14 Nov, a bright moonlit night — careful: do not claim Bromide would have saved it), effective at Birmingham (19 Nov) — the number that mattered was the receiver's filter, not the transmitter's power: experiment 2 again
- Feb 1941, Y-Gerät / DOMINO: ranging by re-radiation; DOMINO re-radiates the return from the BBC's dormant television transmitter at Alexandra Palace (45 MHz) with a shifted phase — broadcasting turned electronic warfare (T); the photos on the right: the BBC's tower at Alexandra Palace, home of the first regular high-definition television service (1936), and its mast — today and in 1975
- the close: radio navigation, not radar — the first fully fought electronic war; the cycle intercept → understand the receiver → jam, spoof → counter is figures/escalation.svg, for questions
- sources: Jones, Most Secret War (1978), pp. 127–129, 151, 164, 175–177; Price, Instruments of Darkness (1977), pp. 44–49
- bridge: "listen to the other side long enough and you hear signals nobody meant to send"
:::

# Signals You Didn't Mean to Send<br>communications → radar → SIGINT → TEMPEST → passive diagnostics {#unintended}

:::place
ladder: 0.0357 0.1250 0.4500 0.8000
spikes: 0.5150 0.0200 0.4493 0.2700
mixer: 0.6209 0.2900 0.2000 0.3720
scope: 0.8284 0.2900 0.1263 0.3720
cap43: 0.6209 0.6410 0.3339 0.0450
kuhn: 0.6209 0.7000 0.1506 0.2170
cap85: 0.6209 0.9080 0.2300 0.0600
:::

:::ladder {notes=off fit}
![who meant the signal: communications, radar, SIGINT, TEMPEST, passive diagnostics — ever less intent on the emitter's side](figures/inference-ladder.svg)
:::

:::step

:::mixer {notes=off fit}
![the Bell Telephone 131-B2 station: a teletype beside the mixer cabinet with its key-tape unit, from the War Department manual TM 11-2209](media/bell-131b2-tm11-2209.webp)
:::

:::scope {notes=off fit}
![a DuMont 208-B cathode-ray oscilloscope of about 1943](media/dumont-208b-oscilloscope.webp)
:::

:::cap43 {notes=off size=caption}
1943: Bell Labs' 131-B2 cipher mixer — and an oscilloscope across the lab[^tempest]
:::

:::spikes {notes=off fit}
![the plain text ATTACK as teletype code; on the line, mixed with a one-time key, unreadable; on an oscilloscope across the lab, a spike at every step of the plain text: readable](figures/tempest-spikes.svg)
:::

:::step

:::kuhn {notes=off fit}
![text from a laptop screen, reconstructed from its radiation 10 m away through three walls (Kuhn, 2003); the text quotes van Eck's 1985 paper](media/kuhn-2003-screen-through-walls.webp)
:::

:::cap85 {notes=off size=caption}
1985: van Eck reads a screen with a TV set — 2003: Kuhn, through three walls[^kuhn]
:::

[^tempest]: National Security Agency, "TEMPEST: A Signal Problem," *Cryptologic Spectrum*, 1972 (declassified 2007). [Online]. Available: https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/cryptologic-spectrum/tempest.pdf; photos: War Department, TM 11-2209 (1946), Fig. 1, public domain; DuMont 208-B, Harvard Putnam Gallery, Daderot, CC0, Wikimedia Commons.
[^kuhn]: W. van Eck, "Electromagnetic radiation from video display units: An eavesdropping risk?" *Computers & Security*, vol. 4, no. 4, pp. 269–286, 1985; M. G. Kuhn, "Compromising emanations: eavesdropping risks of computer displays," Univ. of Cambridge, Tech. Rep. UCAM-CL-TR-577, 2003, Fig. 4.3 (not cleared, talk only).

:::notes
- the ladder, read top to bottom: communications (I send so you recover it) → radar (I send and read the echo) → SIGINT (I read what you sent, more than you meant) → TEMPEST (your machine sends what it never meant to) → passive diagnostics (a system radiates its state) — the same inverse problem, ever less intent at the emitter; different ethics, the same mathematics
- click 1, 1943: a Bell engineer sees a spike on a distant oscilloscope each time a teletype cipher machine steps — the plain text can be read from the spikes (NSA, "TEMPEST: A Signal Problem", 1972)
- click 2: 1985, van Eck reads a screen with modified TV equipment; Kuhn 2003, through three walls — the end of the secret, the start of a public field
- careful: TEMPEST is the programme's name; the phenomenon is compromising emanations
- bridge: "turn it around — a complex system's signals tell more about its state than it was built to report"
:::

# {#gremlin master=title-logo}

:::layout
background: wavepackets
:::

:::place
eye: 0.3559 0.1900 0.2906 0.2667
name: 0.1875 0.5706 0.6250 0.1419
link: 0.1897 0.7233 0.6000 0.1200
:::

:::eye {notes=off fit}
![the iRIS eye: the iris between two blue eyelids](figures/iris-eye.svg)
:::

:::name {notes=off fit}
![GREMLiN](figures/GREMLIN_wordmark.svg)
:::

:::link {notes=off size=150%}
[[https://fair-acc.github.io/gremlin/](https://fair-acc.github.io/gremlin/)]{colour=#ffff00}<br>[[https://www.irisproject.eu/](https://www.irisproject.eu/)]{colour=#ffff00}
:::

:::notes
- 30 s, a flash: the ladder's last rung, today — GREMLIN: one sensor on a facility's mains feed → which devices run, which drift, which are about to fail
- the same philosophy, scaled from one sensor to a distributed system: the next talk in this session, 15:10
- bridge: "how do we look at a signal at all? two ways — and for a century engineers have reasoned in both"
:::

# Pulses or Spectra?<br>two ways of seeing the same signal — and for a century engineers have reasoned in both {#duality master=people}

:::place
fig: 0.0357 0.1250 0.8000 0.4770
braid: 0.0357 0.6350 0.8000 0.3360
people: 0.8607 0.0190 0.1143 0.8667
:::

:::fig {notes=off fit}
![the same three signals in time and in frequency: a click is a flat wide spectrum, a steady tone one sharp line, a train of bunches a comb of lines under the bunch's envelope; time tells when, frequency which tone](figures/time-frequency.svg)
:::

:::braid {notes=off fit}
![the braid to 1950 with its milestones sorted by view: in gold above, frequency — the superheterodyne, the Lorenz beam's modulation, the klystron's resonance; in white below, time — sound ranging's arrival times, radar's pulse ranging, the delays of Gee and LORAN](figures/braid-duality.svg)
:::

:::people {notes=off size=40% fit}
![Carl Friedrich Gauss](media/portraits/gauss.webp)

[**Carl Friedrich Gauss**]{size=205%}<br>[1777–1855]{size=205%}

![Joseph Fourier](media/portraits/fourier.webp)

[**Joseph Fourier**]{size=205%}<br>[1768–1830]{size=205%}

![James Cooley and John Tukey](media/portraits/cooley-tukey.webp)

[**Cooley, Tukey**]{size=205%}<br>[the FFT, 1965]{size=205%}
:::

:::notes
- the picture does it, no Fourier lecture: a click is every frequency at once, a steady tone is one line, a train of bunches is a comb — Schottky and the MIM come back to the comb
- the portraits: Gauss found the fast algorithm in 1805 and left it unpublished; Cooley and Tukey reinvented it in 1965 — an idea that had to be found twice
- the strip: the same history sorted by view — time (sound ranging, radar pulses, LORAN) and frequency (superheterodyne, modulation, resonance); accelerators inherit both
- bridge: "next, the tuning fork — the same delay, measured the other way, and where that way breaks"
:::


# Experiment 3: Detection by Phase<br>no edge to time, one line to find{#exp2}

:::place
live: 0.0357 0.1250 0.9286 0.7250
toolbar: 0.3500 0.8550 0.6143 0.0900
card: 0.0250 0.5200 0.3325 0.3600
decca: 0.0357 0.5280 0.3150 0.4300
:::

:::gr4
id: exp2
region: live
workflow: workflows/exp2-noise-tone.grc
lifecycle: run-while-visible
toolbar: toolbar
:::

:::card {notes=off fit layer=above}
![a piece of the chalkboard over the live region's placeholder pane](figures/chalk-patch-left.webp)
:::

:::decca {notes=off size=caption fit layer=above}
![a Decca Navigator Mk 12 receiver: a chain selector and three dials, the decometers, in red, green and purple, each counting lanes and the fraction of a lane](media/decca-navigator-mk12.webp)

Decca, from 1944: its dials count the lanes the phase cannot[^ph-decca]
:::

[^ph-decca]: Decca Navigator Mk 12, photo: Stahlkocher, CC BY-SA 3.0, via Wikimedia Commons.

:::notes
- the message: a steady tone has no edge to time, but it has a phase — finer than any edge, but it loses count of the cycles; the spectra way, and where it breaks
- `input`: simulation (a 160 Hz tone, struck once a second, the source circling) or the microphones; the `tone` choice switches to 440 Hz, the fork
- three beats, no clicks:
  1. strike the fork: one bright line in the waterfall at once — a weak tone invisible in a trace is still one line in the spectrum (keep that: on `schottky` a beam is found the same way)
  2. the traces: four shifted copies of one sine — the shift is the delay, but which crest belongs to which?
  3. the correlation: the drum's was one sharp peak; a tone's is a cosine, peaks one period apart — the phase says where within a period, not which period; at 160 Hz the gold estimate follows the source, at 440 Hz the hyperbolae jump to ghosts
- optional, dragging the band onto the line: the noise goes, the ghost stays — a filter cannot find the lost cycle
- bottom left, the same lesson at sea: Decca's dials count the lanes the phase cannot — and every phase-locked loop counts its cycle slips: two fields, two names — lanes and cycle slips — for one problem
- Δt = Δφ / 2πf₀, modulo one period; the cure is bandwidth (experiment 4)
- bridge: "holding a phase to a fraction of a cycle is what every accelerator cavity does — and the tubes that drive them went to war first"
:::

# The Klystron Goes to War and Comes Home<br>an accelerator's cavity turned RF source — radar gave back receivers and pulsers, the accelerators tubes, timing and detectors {#loop}

:::place
fig: 0.0357 0.1250 0.4800 0.7000
credits: 0.0357 0.8300 0.4800 0.0900
trades: 0.5300 0.1250 0.4343 0.7300
tcap: 0.5300 0.8550 0.4343 0.0650
:::

:::fig {notes=off fit}
![one loop of photographs, clockwise: 1937 the klystron at Stanford (Hansen's cavity, the Varians' tube) goes into radar (the people at the tubes, 1940–45), comes home to the linacs (the Stanford Mark III, 1950) and is driven beyond radar's needs (SLAC's 245 klystrons, 1966); in the centre, Berkeley 1947: surplus SCR-268 radars set the Alvarez linac's 200 MHz](figures/radar-loop.svg)
:::

:::credits {notes=off size=85%}
the klystron's loop: Stanford's linacs[^slac7731], [^slac2mile]; Berkeley's surplus SCR-268s[^slac3221] · photos[^ph-loop]
:::

:::step

:::trades {notes=off fit}
![what radar and the accelerators traded besides the klystron's loop: radar to accelerators — the superhet receiver in BPM and LLRF electronics (C), monopulse Σ/Δ to the 1981 BPM processors, Rad Lab pulsers to SLAC's modulators, the wartime magnetron to the S-band and medical linacs, surplus SCR-268s to the Alvarez linac, radar's spectrum analyser to the ISR's Schottky noise (C), radar receiver boards to the Tevatron BPMs; and back, in gold — Hansen's accelerator cavity to the radar oscillator (1938), Oliphant's cyclotron lab to the cavity magnetron (1940), Lawrence's cyclotroneers to the Rad Lab, linac klystrons to the BMEWS and Goldstone radars (1959), collider trackers to the Fermi gamma-ray telescope (2008), CERN pixel chips to the ISS radiation monitors (2012), White Rabbit timing to the EISCAT_3D radar (2022)](figures/radar-trades.svg)
:::

:::tcap {notes=off size=125%}
same problem — different domains[^trades], [^back]
:::

[^slac7731]: G. Caryotakis, "The Klystron: A Microwave Source of Surprising Range and Endurance," SLAC-PUB-7731, 1998. [Online]. Available: https://www.slac.stanford.edu/pubs/slacpubs/7500/slac-pub-7731.pdf
[^slac3221]: SLAC-PUB-3221, "Elementary Principles of Linear Accelerators," 1983. [Online]. Available: https://www.slac.stanford.edu/pubs/slacpubs/3000/slac-pub-3221.pdf
[^slac2mile]: R. B. Neal (ed.), *The Stanford Two-Mile Accelerator*, ch. 1–3. New York: Benjamin, 1968. [Online]. Available: https://ahro.slac.stanford.edu/sites/default/files/2024-08/Chapters_1_3.pdf
[^back]: G. Caryotakis, SLAC-PUB-7731, 1998 (the cavity, the Mark III klystrons in BMEWS); A. E. Siegman, "Edward L. Ginzton," NAS Biographical Memoirs; W. B. Atwood et al., "The Large Area Telescope on the Fermi Gamma-ray Space Telescope," *Astrophys. J.*, vol. 697, p. 1071, 2009; L. Pinsky et al., Timepix-based radiation environment monitors on the ISS, *J. Radiat. Res.*, vol. 55, 2014; EISCAT_3D synchronisation tender, 2022 (White Rabbit, CERN WR switch v3).
[^ph-loop]: Photos, via Wikimedia Commons, public domain: "Prototype klystron cutaway," *Electronics*, vol. 13, 1940; Flt Lt Goodchild, RAF, "WAAF radar operator Denise Miley, Bawdsey, May 1945," IWM CH 15332; US Army Signal Corps, "Radar" (an SCR-268), Casablanca, 1943, NARA 531325; US Office of Naval Research, "Mark III linear electron accelerator," Stanford, early 1950s; US Department of Energy, "SLAC klystron gallery," c. 1968.
[^trades]: R. E. Shafer, "Beam position monitoring," *AIP Conf. Proc.*, vol. 249, p. 601, 1992; S. P. Jachim, R. C. Webber and R. E. Shafer, "An RF beam position measurement module for the Fermilab energy doubler," *IEEE Trans. Nucl. Sci.*, vol. NS-28, p. 2323, 1981; R. B. Neal (ed.), *The Stanford Two-Mile Accelerator*, 1968, modulator chapter, ref. 1: G. N. Glasoe and J. V. Lebacqz, *Pulse Generators*, MIT Radiation Laboratory Series, vol. 5, 1948; C. W. Miller, "An 8-MeV linear accelerator for X-ray therapy," *Proc. IEE*, vol. 101, 1954; M. Chodorow et al., *Proc. IRE*, vol. 47, p. 20, 1959; J. Borer et al., HEACC 1974; the Tevatron BPM upgrade, *JINST* 6 T11005, 2011.

:::notes
- the message: ping-pong, not one-way — Hansen's cavity, conceived to accelerate electrons, became the klystron; it went to war in radar, came home to the linacs, and the linacs drove it far beyond what radar needed
- the loop, clockwise: 1937 Stanford, the klystron → radar, the people at the tubes → 1947–50 the Mark I–III linacs → 1966 SLAC, 245 klystrons on one phase reference: the tuning fork's phase, held along two miles
- the centre: war-surplus SCR-268s set the Alvarez linac's 200 MHz (Alvarez, LINAC'86: the sets' power supplies, not their oscillators)
- careful: the magnetron is a cousin of the cyclotron, not its child (Hull, 1921)
- click: what else crossed, by year — read three rows, not all: the superhet in beam-position monitors; radar's monopulse Σ/Δ in a 1981 Fermilab BPM (citing Skolnik); and back, White Rabbit timing in the EISCAT_3D radar (2022) — same problem, different domains, different words
- bridge: "the arrows on this picture are people — and people are the next slide"
:::

# The People Cross the Boundaries<br>knowledge moved because people moved — and many of the moves were driven by war {#people}

:::place
l0: 0.0100 0.1050 0.9800 0.8850
l1: 0.0100 0.1050 0.9800 0.8850
:::

:::l0 {notes=off fit}
![careers drawn like a transit map between six fields, 1905–1965, a portrait at each line's start and the name at its end: W. L. Bragg from X-rays to sound ranging and back to crystals; John Randall from phosphors to the cavity magnetron and to King's College, DNA by X-rays; Hansen and the Varians and Luis Alvarez from accelerators to radar and back](figures/people-lines-0.svg)
:::

:::step

:::l1 {notes=off fit}
![twenty-three more lines over the same lanes, almost all bending in a war — Hertz and Rutherford from radio; the sonar people Boyle, A. B. Wood, Fessenden, G. W. Pierce, Barkhausen; Jansky's radio astronomy; W. H. Bragg to anti-submarine acoustics; the French connection — Nordmann and Esclangon from the Paris Observatory to sound ranging and back, Langevin's ultrasonic sonar, Rocard from radio to radar to radio astronomy; Tuve, Bowen, Lovell, Oliphant, McMillan, Cockcroft, Touschek, Blumlein, Reeves, Kompfner](figures/people-lines-1.svg)
:::

:::notes
- the picture says it without words: nearly every line bends inside a war band — war moved people; almost none starts there — war accelerated, it did not invent
- the four with medallions, one clause each: Bragg (crystals → sound ranging → crystals); Randall (phosphors → the magnetron → the biophysics unit where DNA's X-ray pictures were taken); Hansen and the Varians (the cavity → the klystron → radar → the linac); Alvarez (cyclotron → Rad Lab → the surplus-radar linac)
- click: twenty-three more — texture, ten seconds; name three as the lines arrive: Esclangon and Nordmann, two astronomers with the same idea in autumn 1914; Fessenden, radio pioneer, whose oscillator heard an iceberg's echo (1914); Kompfner, an architect who invented radar's travelling-wave tube, which flew in Telstar
- careful: "Watson-Watt invented radar" — radar was developed independently in several countries; Randall and Boot's magnetron was the one that worked at kilowatts and crossed the Atlantic, not the first
- the line to end on: "the arrows of the braid are people"
:::

# The Braid So Far: to 1950<br>radio, radar and accelerators trade parts and people — the instruments are still valves {#strands1950}

:::place
fig: 0.0357 0.1300 0.9286 0.7500
:::

:::fig {notes=off fit}
![the braid up to 1950: the superheterodyne, Ising and Widerøe, Cockcroft–Walton, the Lorenz beam, the klystron, the magnetron and Knickebein, the betatron, Gee and LORAN, the Alvarez linac](figures/braid-1950.svg)
:::

:::notes
- 20 s: thirty years of radio, radar and accelerators trading parts and people — the labels are the act just told
- the WWII band holds many of the crossings, not all: the cyclotron and the klystron came before it
- the instruments strand is still cyan — valves, film, cathode-ray tubes; the superhet's mixer and filter are a multiply and a filter in a software radio today
- next: noise that is information
:::

# Schottky: Somebody's Noise is Somebody Else's Signal<br>Hear Particle Beams without touching — then act on it: Antiprotons, the W and Z — and single Ions today {#schottky master=people}

:::place
s1: 0.0357 0.1250 0.5000 0.2650
t1: 0.5550 0.1350 0.2800 0.2400
isr: 0.0357 0.4000 0.2300 0.4600
cool: 0.2750 0.4000 0.2700 0.4600
esr: 0.5400 0.3300 0.3100 0.5600
people: 0.8607 0.0190 0.1143 0.8667
medal: 0.9577 0.5954 0.0350 0.0622
:::

:::s1 {notes=off fit}
![Schottky noise as a spectrum: one particle gives a comb of lines at the revolution harmonics; N particles with a momentum spread give bands whose width grows with the harmonic, the betatron sidebands beside them — the tune](figures/schottky-strip.svg)
:::

:::t1 {notes=off}
**1918**: shot noise *is* information[^schottky] — a ring's noise tells its momentum spread and tune: **hear the beam without touching it**
:::

:::people {notes=off size=40% fit}
![Walter Schottky](media/portraits/schottky.webp)

[**Walter Schottky**]{size=205%}<br>[1886–1976]{size=205%}

![Simon van der Meer](media/portraits/van-der-meer.webp)

[**Simon van der Meer**]{size=205%}<br>[1925–2011]{size=205%}
:::

:::isr {notes=off size=caption fit}
![the first longitudinal Schottky scans of the ISR, 1972: the beam's distribution in both rings, read from its noise](media/isr-schottky-1972.webp)

**hear** — the ISR, 1972: the first Schottky scans[^borer]
:::

:::step

:::cool {notes=off size=caption fit}
![stochastic cooling: a pickup hears the beam's noise, an amplifier, and a kicker across the ring kicks it away; the signal takes the short cut and meets the particles it heard; beneath, 1968 the idea, 1974 the ISR test, 1980 the antiproton accumulator, 1983 the W and Z, 1984 the Nobel Prize](figures/stochastic-cooling.svg)

**act** — van der Meer: dense antiprotons, the W and Z[^vdm]
:::

:::medal {notes=off fit}
![a Nobel Prize medal](media/nobel-medal.webp)
:::

:::step

:::esr {notes=off fit}
![a Schottky spectrogram of GSI's ESR, as in the GREMLIN talk: "Nuclear Physics: Two Body Decay" — a single 142Pm60+ ion's line ends at its electron capture and the 142Nd60+ daughter's line appears, the recoil of the emitted neutrino visible as the line's jump (Kienle, Bosch et al. 2013)](figures/schottky-decay-gremlin.svg)
:::


[^schottky]: W. Schottky, "Über spontane Stromschwankungen in verschiedenen Elektrizitätsleitern," *Ann. Phys.*, vol. 362, no. 23, pp. 541–567, 1918.
[^borer]: J. Borer, P. Bramham, H. G. Hereward, K. Hübner, W. Schnell and L. Thorndahl, "Non-destructive diagnostics of coasting beams with Schottky noise," in *Proc. 9th Int. Conf. High Energy Accelerators*, Stanford, CA, USA, 1974, pp. 53–56; the 1972 scans: CERN Annual Report 1972, p. 109, as reproduced in P. J. Bryant, "The impact of the ISR on accelerator physics and technology," CERN, 2012, arXiv:1206.3950, Fig. 16, CC BY 3.0.
[^vdm]: S. van der Meer, "Stochastic damping of betatron oscillations in the ISR," CERN, Geneva, Switzerland, Rep. CERN/ISR-PO/72-31, 1972.

:::notes
- the message: noise is information — a ring hears its own beam without touching it, and once you can hear it you can act on it; somebody's noise is somebody else's signal
- Schottky, 1918: shot noise tells about the discrete carriers — the same year he patents the superheterodyne, invented three times, independently (Lévy, Armstrong, Schottky: co-evolution)
- top strip: one particle passing a pickup is a comb; many with a momentum spread make bands; the sidebands are the tune — read without touching the beam (the word comes from Kerst's betatron)
- **hear**: the ISR, 1972 — the first Schottky scans of a beam, with Schottky's formula applied by name (T)
- click 1, **act**: van der Meer — measure the noise here, kick it away there: stochastic cooling is feedback; dense antiprotons → the W and Z (1983) → Nobel 1984
- careful: the ISR signals did not *cause* the idea (van der Meer had it in 1968); Widrow's adaptive noise cancelling (1975) is the parallel invention outside the field (P)
- click 2, **count**, our machine: in GSI's storage ring every ion draws its own line — a single ion's decay seen as one line ending and another appearing; careful: the 2008 "GSI oscillations" were not confirmed
- careful: Schottky spectra and passive RF/SIGINT share the maths, not a lineage — "parallel"
- bridge: "the sidebands show the slow motion of the whole beam; inside one bunch it is fast — and to see it we split the band before the ADC"
:::

# Same Answer, Twice: Split the Band Before the ADC<br>radio does it in software, the MIM in copper — found independently {#mim}

:::place
ht0: 0.0357 0.1350 0.1888 0.3600
ht1: 0.2320 0.1350 0.1888 0.3600
htcap: 0.0357 0.4950 0.3851 0.0750
ear: 0.0357 0.5800 0.3600 0.3850
fig: 0.4375 0.0553 0.5268 0.4930
proto: 0.5060 0.5409 0.2240 0.2854
pcb: 0.7400 0.5409 0.2240 0.2854
:::

:::ht0 {notes=off fit}
![head-tail oscillation, mode m = 0, χ = 0, CERN PS Booster, 1974: many turns of the bunch's difference signal on an oscilloscope](media/headtail-m0-psb-1974.webp)
:::

:::ht1 {notes=off fit}
![head-tail oscillation, mode m = 1, χ = 6.9, CERN PS Booster, 1974: head and tail swinging in antiphase](media/headtail-m1-psb-1974.webp)
:::

:::htcap {notes=off}
ex. PS Booster, 1974[^mim]: head-tail betatron motion inside one particle bunch.<br>LHC: 1 kV carrier, 1 ns long, "AM/FM"-modulated @ $\scriptstyle 10^{-6}$!
:::

:::ear {notes=off size=caption fit}
![the ear as a filter bank: sound reaches the eardrum, the ossicles pass it to the cochlea, whose hair cells are each tuned to one frequency, from 20 kHz at the base to 20 Hz at the apex](figures/cochlea.svg)

the ear splits the band first; the cochlear radio copies it[^cochlea]
:::

:::fig {notes=off fit}
![the same bunch spectrum twice: OFDM covers it back to back with many bands; the MIM samples it only at the baseband and at multiples of the RF frequency, enough to rebuild the bunch in software](figures/split-band.svg)
:::

:::proto {notes=off size=caption fit}
![the MIM proof-of-concept prototype, 2012: microstrip filters, amplifiers and diode-detector boards in one chassis](media/mim-prototype-2012.webp)

2012 prototype: SPS, LHC
:::

:::pcb {notes=off size=caption fit}
![the 16-band MIM filter bank, 2013: microstrip band-pass filters and splitters etched on one copper board](media/mim-filterbank-16-2013.webp)

2013 16-band prototype[^mim]
:::

[^mim]: R. J. Steinhagen, M. J. Boland, and T. G. Lucas, "A Multiband-Instability-Monitor for high-frequency intra-bunch beam diagnostics," *Proc. IBIC2013*, Oxford, paper and talk TUBL3, CC BY 3.0; CERN-ACC-2013-0294; the head-tail traces: J. Gareyte, "Head-tail type instabilities in the PS and Booster," CERN, 1974.
[^cochlea]: S. Mandal et al., *IEEE J. Solid-State Circuits* 44(6), 2009; D. F. Albuquerque et al., *Proc. IEEE IMWS*, 2010; OFDM: R. W. Chang, *Bell Syst. Tech. J.* 45(10), 1966; S. B. Weinstein and P. M. Ebert, *IEEE Trans. Commun. Technol.* 19(5), 1971.

:::notes
- co-evolution is not only a story about famous people a century ago — it happens now
- the wall: the head and tail of a 1 ns LHC bunch move differently; seeing that in time needs 6–12 GHz, and no ADC that fast has the bits — waiting for a better ADC does not help
- the radio answer: OFDM — many overlapping, orthogonal sub-carriers, split after one ADC by an FFT; every Wi-Fi and LTE receiver in this room does it
- the MIM answer: a short bunch's spectrum is fixed by a few narrow bands at multiples of the RF — split them first, in copper, before any ADC, then slow 24-bit ADCs: nanometre motion at the onset of an instability
- the ear did it first: the cochlea is a filter bank before any "ADC"; the RF "cochlear radio" found the same answer
- the acoustic thread: Tucker's microphone was one tuned resonator; the cochlea a bank of them; the MIM sixteen of them in copper
- careful: with OFDM say "the same idea" (P); the cochlear radio is co-evolution (C) — "independently studied", says the 2013 paper; never draw an arrow from either to the MIM
- only after the comparison, understated: "there is a reason I picked this example — this was our MIM development at CERN"
- bridge: "so far we only listened; the last experiment sends its own signal — a chirp, and a receiver that knows it"
:::

# Experiment 4: Finding a Signal Below the Noise<br>known chirp in the noise — trick behind LoRa, GPS and long-range radar {#exp6}

:::place
live: 0.0357 0.1250 0.9286 0.7250
toolbar: 0.3500 0.8550 0.6143 0.0900
card: 0.0250 0.5200 0.3325 0.3600
pc: 0.0357 0.5280 0.3150 0.3300
pccap: 0.0357 0.8650 0.3150 0.0700
:::

:::gr4
id: exp6
region: live
workflow: workflows/exp6-chirps-recorded.grc
lifecycle: run-while-visible
toolbar: toolbar
:::

:::card {notes=off fit layer=above}
![a piece of the chalkboard over the live region's placeholder pane](figures/chalk-patch-left.webp)
:::

:::pc {notes=off fit layer=above}
![pulse compression: the known chirp, 1 to 8 kHz in 20 ms, correlated with itself becomes one sharp peak at the delay; time-bandwidth product 140, a gain of 21 dB](figures/pulse-compression.svg)
:::

:::pccap {notes=off size=caption}
radar's answer: a long pulse with the resolution of a short one — pulse compression, built on the matched filter (North 1943)[^north]
:::

[^north]: D. O. North, "An analysis of the factors which determine signal/noise discrimination in pulsed-carrier systems," RCA Laboratories, Rep. PTR-6C, June 1943; reprinted in *Proc. IEEE*, vol. 51, no. 7, pp. 1016–1027, 1963.

:::notes
- said first: a GPS signal arrives some 20 dB below the receiver's noise — it works only because the receiver knows the code it is looking for and correlates; this slide shows it with sound
- the rehearsal take (recorded — say so): a known chirp, 1–8 kHz in 20 ms, once a second; the noise rises until the chirp is gone from the four traces — the matched filter's peak stays, the ranging keeps working: "the shakers again — and this time the receiver knows what it is looking for"
- stop listening, start asking: Bragg waited for the gun; radar chooses its probe — the bandwidth gives back the delay the tuning fork lost, the correlation gives the gain (20 ms × 7 kHz = 140, ~21 dB)
- the echo, said slowly — one receiver, many names: radar's matched filter (North 1943) and pulse compression; the GNSS code correlator; Wi-Fi's preamble search; sonar; the accelerator's swept-excitation measurement [verify: a GSI/CERN example to cite] — the same principle, not a lineage
- careful: chirp radars came later than North's matched filter [verify: Klauder et al., Bell Syst. Tech. J. 39, 1960]
- bridge: "nothing on this laptop is new: Tucker's band-pass, Bull's trigger, Bragg's and LORAN's fit, North's matched filter, Gauss's FFT — put the 140 years on one picture"
:::

# Not a Tree — a Braid<br>140 years, three kinds of crossing: transfer, co-evolution, parallel invention — most arrows are people {#braid}

:::place
base: 0.0100 0.1050 0.9800 0.8150
line: 0.0357 0.9250 0.8000 0.0500
:::

:::base {notes=off fit}
![the braid, 1865–2026: five strands — waves as instruments, acoustics, radio and radar, accelerators, signal processing — with their milestones and the crossings between them: documented transfers as solid arrows, co-evolution dashed, the same maths dotted; the signal-processing strand turns from cyan to gold and ends at the GNU Radio 4.0 logo](figures/braid.svg)
:::

:::line {notes=off size=125%}
**The waves have not changed. What changed is where we put the intelligence.**
:::

:::notes
- let the picture speak; say three things, not every arrow:
- not a tree, a braid: ideas crossed, co-evolved and ping-ponged between the fields — three kinds of crossing: transferred (solid — most are a person packing a suitcase), co-evolved (dashed — Widerøe ‖ Walton, the MIM ‖ the cochlear radio), parallel (dotted — the hyperbolae of sound ranging and LORAN: "the dotted ones we must not over-claim")
- the forks: one goal, two routes — the first to succeed was not always the one that scaled, and both usually survive
- the bottom strand turns from cyan to gold: wire, brass, film and valves became software — everything on this laptop today is its gold end
- read the line at the bottom once, then the close
:::

# Echoes from the Past into the Future …<br>…learn from it twice {#learn master=title-logo}

:::place
head: 0.0357 0.0400 0.6400 0.0900
sub: 0.0357 0.1400 0.6400 0.0700
pop: 0.0357 0.2850 0.4400 0.3900
lep: 0.5050 0.2850 0.4400 0.3900
bleuet: 0.0357 0.6680 0.0420 0.0750
c1: 0.0820 0.6700 0.4400 0.3000
c2: 0.5050 0.6700 0.4400 0.3000
c3: 0.5050 0.8200 0.4400 0.0700
ask: 0.0357 0.8650 0.7800 0.0550
contact: 0.0357 0.9300 0.7800 0.0450
:::

:::layout
logo: media/gnuradiodays-2026-banner-cutout.webp
:::

:::contact {notes=off}
[Ralph J. Steinhagen · GSI/FAIR, Darmstadt, Germany · [https://github.com/fair-acc/gnuradio4](https://github.com/fair-acc/gnuradio4)]{colour=#ffff00}
:::

:::pop {notes=off fit}
![poppies before the Thiepval Memorial to the Missing of the Somme](media/poppies-thiepval.webp)
:::

:::lep {notes=off fit}
![the author in front of a copper LEP accelerating cavity with its spherical storage cavity, on display at CERN](media/lep-cavity-steinhagen.webp)
:::

:::bleuet {notes=off fit}
![the Bleuet de France, the French flower of remembrance](figures/bleuet-de-france.svg)
:::

:::c1 {notes=off size=150%}
**as citizens** — remember, keep the memory alive,<br>— so that it never happens again
:::

:::c2 {notes=off size=150%}
**as engineers and scientists** — shared language, shared tools,<br>the fundamentals taught: so that good ideas cross before we reinvent them
:::

:::c3 {notes=off size=150%}
— and understand why an idea failed in the past<br>— with today's tools, it may echo to the present and deserve a second look
:::

:::ask {notes=off size=160%}
[**Questions? Let's talk — what do you call this in your field?**]{colour=#ffff00}
:::

:::notes
- the title's echoes once more: the bracket `flanders` and `problem` opened closes — the same poppies, and a LEP cavity, the klystron's lineage (my own photo)
- as citizens: remember, keep the memory alive — the war accelerated the crossings, it did not invent them
- as engineers and scientists: the same problems recur in every field under different names; specialisation is necessary, isolation is expensive — shared language, shared tools and the fundamentals taught let good ideas cross before we reinvent them; Widerøe, alone and cut off, is the counter-example
- relive it to understand it: some experiments must be re-done by every generation — Tucker's band-pass, Bull's trigger, North's matched filter ran again in this room — to be understood, not just known; know why an idea failed, and with today's tools it may deserve a second look: the ray-transformer failed twice, then worked; the MIM went back to analogue filter banks
- said last (unattributed): "Everybody makes mistakes … the wise learn from the mistakes of others. So let's share our experience, our ideas, our aspirations — and our wisdom."
- the question: ask three communities in the room to name the matched filter, the TDOA solver and the feedback loop in their own words
:::

# References {#references master=blank}

:::place
list: 0.0200 0.0950 0.9600 0.8800
:::

:::list {size=80%}
:::references 1-22
qr: https://github.com/fair-acc/gnuradio4
label: GNU Radio 4
:::
:::

:::notes
- every work the deck cites, numbered as on its slides, in two parts (`:::references 1-22`, then `23-`), right after the close; the backups follow; portraits: sources in media/portraits/PORTRAITS.md; picture credits in media/CREDITS.md
:::

# References cont'd {#references2 master=blank}

:::place
list: 0.0200 0.0950 0.9600 0.8800
:::

:::list {size=80%}
:::references 23-
qr: https://github.com/fair-acc/gnuradio4
label: GNU Radio 4
:::
:::

:::notes
- the second half of the references, with the same QR codes; the links of the citation marks lead to whichever of the two slides lists the number
:::

# Backup — The Braid, 2026<br>the instruments strand turned gold — wire, brass, film and valves became blocks in a flow graph {#strands2026}

:::place
fig: 0.0357 0.1300 0.9286 0.7500
:::

:::fig {notes=off fit}
![the braid up to 2026: the instruments strand turns from cyan to gold between the FFT, the software radio and GNU Radio; the GNU Radio 4.0 logo at the strands' end](figures/braid-2026.svg)
:::

:::notes
- the instruments strand turns gold from the 1960s: the FFT (1965), the software radio (1990s), GNU Radio (2001), GNU Radio 4.0
- backup since round 52 (the main line ends on `braid`): no arrows on the slide, and no list — only the colour, cyan to gold
- the strands do not merge: physics, radio and radar stay separate fields; what they increasingly share is the instruments strand — and that we can maintain together, in the open
- also on this stretch: van Eck (1985), White Rabbit (2008), the cochlear radio and the MIM (2009–13)
- also on the accelerators strand now: the ISR (1971, Schottky's noise heard from a beam), the Sp̄pS (1981), LEP (1989), the LHC (2008), FAIR — and the FCC, perhaps (;-)
- next: the whole braid in detail
- 30 s
:::

# Backup — The Echoes Remain<br>the same instruments, re-labelled in today's language {#echoes master=double}

:::layout
grid: [(text)]
:::

:::text {notes=off size=90%}
| the first time | the rhyme, today |
| --- | --- |
| 1887 Hertz: spark gap, resonant loop | an SDR: generate, detect, characterise |
| 1917 sound ranging: film, hot wire | four microphones, ADC, band-pass, TDOA |
| 1918 Schottky: noise is information | spectral estimation, single ions |
| 1924–40 Ising, Widerøe, Kerst: RF in phase | LLRF holds the phase; the tune |
| 1932–43 Lorenz beam; Gee, LORAN | ILS, VOR; GNSS |
| 1940 Knickebein: the receiver's filter | jam the receiver, not the beam |
| 1937–50 klystron: Stanford → radar | klystron linacs, superhet BPMs |
| 1943 North: the matched filter | pulse compression, GNSS, Wi-Fi |
| 1943 Bell Labs: a cipher mixer's spikes | TEMPEST → GREMLIN |
| 1966 OFDM, 2009 cochlear radio | 2013 MIM: sixteen bands in copper |
:::

:::right {notes=off}
![three domains around one RF and DSP core](figures/three-domain.svg)

**History doesn't repeat, but it often rhymes.**
:::

:::notes
- read two or three rows, not all: the drum and the band-pass heard tonight are 1917 in software; one row runs backwards — radio had OFDM and the cochlear radio first, the MIM found the same answer in copper in 2013
- the quotation, unattributed on purpose: the earliest known form is Theodor Reik, 1965 ("… it merely rhymes"); "said Mark Twain" first appears in 1970 (J. R. Colombo), sixty years after his death; Twain and Warner only wrote "History never repeats itself" (*The Gilded Age*, 1874) — Quote Investigator, 2014
- claim discipline as on `braid`: transfer, co-evolution, parallel invention per row — most transfers are a person moving (`people`); the parallel rows share the maths, not a lineage: say "rhymes", never "descends from"
- background, not said — rows to slides (T transfer, C co-evolution, P parallel): Hertz `hertz`/`chain` T · sound ranging `problem`/`exp1`/`lowpass` P (Bragg's X-ray phase → acoustics T) · Schottky `schottky` T · Ising/Widerøe/Kerst `widero`/`betatron` T · navigation `navigation` C · Knickebein `beams` T · klystron `loop`/`people` T (superhet BPMs C) · North `exp6` P · Bell Labs `unintended`/`gremlin` P · MIM `mim` C (advisor, round 56)
:::

[^ph-sr]: K.u.k. Kriegspressequartier, "Schallmess-Hauptstelle von Artillerie-Messzug 506," photograph, Österreichische Nationalbibliothek, via Wikimedia Commons, public domain.
[^ph-allybbc]: Spudgun67, "Television - Alexandra Palace N22," photograph, 2015, via Wikimedia Commons, CC BY-SA 4.0.
[^ph-ally]: S. Howe, "Alexandra Palace TV mast (1975)," photograph, Geograph Britain and Ireland (3732351), via Wikimedia Commons, CC BY-SA 2.0.
[^ph-spl]: Science Photo Library, "Hertz's electromagnetism experiments, 1880s," engraving, image C033/2767, rights-managed, not licensed: talk only. [Online]. Available: https://www.sciencephoto.com/media/811019/
[^ph-hertzlab]: Heinrich Hertz's original apparatus (induction coil, dipole with spheres, resonators, reflector), photograph, Deutsches Museum, Munich.
[^ph-wideroe]: G. Ising, "Prinzip einer Methode zur Herstellung von Kanalstrahlen hoher Voltzahl," *Ark. Mat. Astron. Fys.*, vol. 18, no. 30, 1924, figure as reproduced in P. Waloschek, *The Infancy of Particle Accelerators*, Fig. 3.4; R. Wideröe, "Über ein neues Prinzip zur Herstellung hoher Spannungen," *Arch. Elektrotech.*, vol. 21, no. 4, pp. 387–406, 1928, Bild 1, 6 and 11; reproduced with permission.
[^ph-lorenz]: A. Dahnielson, "Lorenz beam," diagram, Wikimedia Commons, 2010, CC BY-SA 3.0; background removed for the slide.
[^ph-laueapp]: Deutsches Museum, München / Hubert Czech, "Laue apparatus," press photograph, exhibition Atomphysik (not cleared; talk only).
[^ph-laue]: W. H. Bragg and W. L. Bragg, *X Rays and Crystal Structure*. London: G. Bell and Sons, 1915, plate; via Internet Archive Book Images, no known copyright restrictions.
[^ph-rigb]: Royal Institution, "William Bragg's spectrometer," photograph by Paul Wilkinson, © Royal Institution (rights not cleared; talk only). [Online]. Available: https://www.rigb.org/explore-science/explore/collection/william-braggs-spectrometer
[^ph-moerser]: Balcer, "Langer 21 cm Mörser, Hämeenlinna," photograph, 2006, Wikimedia Commons, CC BY 2.5.
[^ph-hinman]: J. R. Hinman, *Ranging in France with Flash and Sound*. Portland, OR: Dunham, 1919, p. 28; public domain, via archive.org.
[^ph-tuckermic]: Science Museum Group, "One Tucker hot-wire microphone," object 1950-190, CC BY-NC-SA 4.0.
[^ph-srgroup]: Royal Institution / Bridgeman Images TRI1768690, c. 1916 (not cleared; talk only).
[^ph-panorama]: Title panorama, left to right: Braggs 1915 plate; K.u.k. Kriegspressequartier, ÖNB; IWM Q 47886; US DOE, "27-inch cyclotron," Livingston and Lawrence, Berkeley; IWM CH 15332; CERN-AC-9102075 © CERN; B. Golda, "Radio Telescope Effelsberg," CC BY-SA 2.0; NASA, GPS satellite; NASA/ESA Hubble, Messier 51 — all via Wikimedia Commons unless stated.
[^ph-cyclotron]: US Department of Energy, "27-inch cyclotron," M. S. Livingston and E. O. Lawrence, Berkeley, 1930s, via Wikimedia Commons, public domain.
