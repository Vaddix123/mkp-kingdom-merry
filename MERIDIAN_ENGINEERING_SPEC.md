# Meridian Data Infrastructure — Reconciled Engineering Spec

> **What this is.** The output of a 30-agent research study + cross-squad conference.
> Thirty agents each researched one non-overlapping lane (power, thermal, water,
> carbon, finance, civil, 3D-render), pulled real equations and sourced numbers,
> and rendered a verdict on Meridian's *claimed* figures. This document is the
> **reconciled** result: contradictions between lanes resolved, duplication
> removed, and a single set of defensible numbers that the 3D model is built from.
>
> Use this as the **single source of truth**. The `CONFIG` block at the end is the
> contract the Three.js model binds to, so the picture and the physics can't drift.

---

## 0. Headline verdict

Meridian is a **genuinely clever synthesis** (behind-the-meter SOFC on stranded
biogas, heat-cascaded to water production, carbon-captured) but the marketed
numbers are **systematically ~15–30% optimistic** and two claims are
**thermodynamically / accounting-unsound as worded** and must be reframed:

| Claim as marketed | Verdict | Defensible restatement |
|---|---|---|
| "Infinity-loop closed cycle" | ❌ Violates 1st/2nd law | Single-pass **exergy-staged** waste-heat cascade; heat ends at rejection |
| "Carbon-negative" | ⚠️ Boundary-dependent | Negative **only** under GWP20 + counting avoided methane; near-neutral under GHG-Protocol/GWP100 |
| "100 MW" | ⚠️ Ambiguous | **~123 MW gross SOFC → ~100 MW... ≈ 70 MW net IT** — pick & label one |
| "Stranded landfill gas" | ⚠️ Off by 10–20× | Needs **multi-landfill biogas hub or pipeline RNG**; one landfill = 3–20 MW |
| "Water-positive" | ✅ *conditionally* | True **only** with dry cooling + multi-effect MD |
| "Returns cleaner effluent" | ✅ *narrowly* | True for the liquid outfall under **ZLD**; salts leave as solid cake |
| CapEx $1.72B | ⚠️ ~15–30% light | Central estimate **~$2.0B** (FOAK) |
| EBITDA $132M | ⚠️ Optimistic | Sober **~$95–110M** unless ≥85–90 MW net IT |
| DSCR 1.80x / 13-yr payback | ⚠️ Mislabeled | 13 yr = unlevered = CapEx/EBITDA; **equity payback ~16–20 yr** |
| 45Q $23M/yr | ✅ Conservative | $27.6M max; $23M fine **if** Class VI storage + prevailing-wage met |

---

## 1. Power & generation (Squad 1)

**SOFC electrical efficiency — use 53% LHV.** Commercial Bloom-class is 54% on
natural gas (lifetime avg); biogas slightly lower. The new 60% figure is the H₂
announcement — optimistic for biogas. Design point: **53% LHV, fuel utilization
85%, cell ≈0.75 V, 0.3 A/cm²**. Size +5–10% modules for degradation (≈0.25%/1000h).

**The "100 MW" must be defined.** Stacking real losses on **123 MW gross SOFC DC**:
−4% inverter, −12–16 MWe carbon-capture parasitic (+~32 MWth steam), −5–10 MW
cooling/MD/BOP ⇒ **~70 MW net to IT** (best case ~75, conservative ~60). To deliver
**100 MW *net IT*** instead, gross SOFC must be **~140 MW**. The model currently
narrates "123 MW gross" — keep that and label net IT honestly.

**Fuel.** At 53% LHV, 100 MW_e gross ≈ **189 MW LHV in ≈ 600–645 MMBtu/hr
≈ ~20,000 scfm of raw LFG** (~500 Btu/scf @ 50% CH₄). One landfill yields **3–20 MW**
(Puente-class ~50 MW is the US ceiling) → Meridian needs a **multi-source biogas
hub or pipeline RNG**. SOFC needs **H₂S < 10 ppbv and siloxanes to ppb** (hard
cleanup constraint). $3/MMBtu is only defensible as *net-of-incentive, raw on-site*
gas (production cost is $11–35/MMBtu before RIN/LCFS/tipping offsets).

**BESS.** 20 MWh = 12 minutes at 100 MW — a power/ancillary asset, **not** backup
energy. Build as **one Tesla Megablock (4× Megapack 3 ≈ 20 MWh)** or 5–6 Megapack 2 XL.
Round-trip ~92%. MISO value: capacity ~$44/kW-yr (2026/27) + regulation ~$17/MWh.
Honest framing: "ancillary-services + grid-interface stabilizer."

---

## 2. Thermal & cooling (Squad 2)

**Heat available ≠ unlimited.** A 123 MW-class SOFC yields **~40 MW_th recoverable**
(33–50 MW range), but the highest-grade heat is consumed internally for reforming/
air-preheat — exported heat is mid-grade. Separately, **IT reject ≈ ~100 MW_th** of
**low-grade (45–60 °C)** heat (two-phase immersion boiling, fluid BP ~49–60 °C).

**The cascade is one-way (this kills "infinity loop").** Heat waterfalls down
temperature tiers and is *consumed* at each step — you cannot reuse a joule:
`SOFC 600–800 °C → steam 150–250 °C → MD feed 80–90 °C → greenhouse/IT-reject 40–60 °C → ambient reject`.
The working *fluid* recirculates; the *energy* does not. Frame as **"single-pass
exergy-staged recovery,"** render the gradient strictly monotonic, and show a
terminal reject branch.

**Heat-demand contention (key reconciliation).** MD wants ~20 MW_th of 80–90 °C;
greenhouse wants up to 30 MW_th (40–60 °C). The ~40 MW high/mid-grade SOFC heat
**cannot do both at full tilt simultaneously** — so: **MD takes the high tier
first**, greenhouse + MD-preheat run off the abundant ~100 MW IT reject (low grade).

**Passive two-phase is only half-true.** Passive at the tank (nucleate boiling +
gravity condensate return) is real; the **secondary condenser loop must be pumped**
at 100 MW. Aggregate vapor ≈ 1,140 kg/s. **PFAS blocker:** 3M ceased Novec/Fluorinert
end-2025 → must specify a **PFAS-free hydrocarbon/HFO dielectric** (flammability review).

**Membrane distillation — multi-effect only.** Single-stage MD (STEC ~700 kWh/m³)
yields only ~620 m³/day per 20 MW_th — too small. **Multi-effect V-AGMD/MEMD
(STEC ~60–100, GOR 6–13)** gives **~4,000–7,000 m³/day per 20 MW_th**. This is the
*enabler* of the water-positive claim; the spec **requires** heat-recovery modules.

**Backstop rejection is mandatory** (energy balance: 100 MW in must leave). Size for
worst case **~100 MW** (summer, greenhouse off). Prefer **dry/adiabatic** coolers:
~0 water (protects water-positive) at ~3.3% parasitic + large footprint. Evaporative
would consume **~1.9 M L/day** and undercut the water claim.

---

## 3. Water & mass balance (Squad 3)

**Stoichiometric water from fuel:** CH₄+2O₂→CO₂+2H₂O = **2.25 kg H₂O / kg CH₄**
≈ **270 L/MWh_e**. At 100 MW, η=0.6, 80% recovery ⇒ **~520 m³/day** recovered
(condensing HX below ~55 °C dewpoint). Real, non-trivial, but not the headline source.

**Site water balance (the reconciliation):**

| Stream | Evaporative-cooling case | **Dry-cooling case** |
|---|---|---|
| MD product | +5,500 | +5,500 |
| Combustion condensate | +520 | +520 |
| Evaporative loss | −1,900 | ~0 |
| Blowdown | −600 | ~0 |
| Process/sanitary/effluent | −450 | −450 |
| **NET m³/day** | **+3,070 (fragile)** | **+5,570 (robust)** |

➡ **Water-positive is defensible ONLY with dry cooling + multi-effect MD.** With
cooling towers it's marketing-fragile. Auxiliary loads (SOFC reforming steam, amine
makeup, sanitary, fire reserve) are immaterial vs MD output **except** SOFC reforming
steam if anode recycle is poor — confirm recycle fraction.

**Effluent.** Salt mass balance is ironclad: salts_in = salts_out. You can discharge
**clean distillate (10–50 ppm < intake)**, but the salts concentrate into brine that
must be **crystallized to solid cake (trucked off-site)** under ZLD (10–50 kWh/m³).
"Cleaner effluent" is true for the *liquid outfall only* — contaminant mass is
exported as solid, not destroyed. Any liquid brine discharge breaks the claim.

---

## 4. Carbon & environment (Squad 4)

**Captured CO₂:** ~**230,000 t/yr** (upgraded biomethane) to ~**410,000 t/yr** (raw
LFG, where ~40% native CO₂ passes through to the flue). **325,000 t/yr is mid-range —
plausible only if counting native LFG CO₂.** Capture penalty ≈ **12–16 MWe + ~32 MWth**
(shared with the electrical parasitic budget — don't double-count). CANSOLV ~90–95%.

**Methane avoided (the dominant climate term, *if* real):** ~100,000 t CH₄/yr →
**~2.5 MtCO₂e (GWP100) / ~7.8 Mt (GWP20)** — an order of magnitude bigger than the
capture. **But only versus a venting counterfactual.** If the landfill is already
required to flare (most US Subtitle-D sites are), this benefit collapses toward zero.
Highly sensitive to GWP timeframe.

**Honest net carbon:** `Net = Scope1_residual − captured − CH₄_avoided + embodied(~22k t/yr)`.
**Carbon-negative is defensible only** under (a) GWP20 **and** (b) a wide boundary
that credits avoided methane (which GHG-Protocol treats as *avoided*, not *removal* —
strict SBTi accounting rejects it toward "negative"). Under GWP100 + honest embodied,
Meridian is **near-neutral to mildly positive**. Render a carbon-balance bar with a
**GWP20/GWP100 toggle** and a **boundary toggle** — do not hard-render "carbon-negative."

**Air quality is a genuine win.** SOFCs are electrochemical → **near-zero NOx/SOx/CO/PM/VOC**
(NOx ~3.9 tpy ≪ 100 tpy PSD threshold) → likely a **minor source**, no SCR/FGD, no big
smokestacks (remove any from the model). Real emission point is the **amine block**
(ammonia/amine slip/nitrosamines) — model an absorber+water-wash with a small vent.

**45Q.** 325,000 t × $85 = **$27.6M gross**; "$23M" is conservative. **Binary on two
flags:** Class VI geologic storage + Subpart-RR MRV, and prevailing-wage/apprenticeship
(5× multiplier; miss it → $17/t → $5.7M). Depict the **injection well + MRV** as the
eligibility-critical asset.

**Greenhouse heat offtake is seasonal.** 30 MW heats **~13 ha at winter peak** (up to
47 ha at average winter load), but **summer demand ≈ 0** (load factor ~0.3) →
realistic annual average **~8–12 MW**, not a steady 30 MW sink. Backstop must absorb
the full 30 MW every summer. CO₂ enrichment (800–1,000 ppm) synergizes with capture.

---

## 5. Finance & site (Squad 5)

**CapEx (bottoms-up):** SOFC fleet ~$500M (100 MW @ $5k/kW) + DC shell/MEP/immersion
~$770M (70 MW IT @ ~$11M/MW) + amine CCS ~$150–200M + BESS ~$50M + gas cleanup ~$45M
+ MD ~$30M + greenhouse ~$8M = **~$1.52B direct**, ×1.30 (EPC + FOAK contingency) =
**~$2.0B central (range $1.95–2.3B)**. $1.72B is **~15–30% light**. SOFC + DC build are
~75% of cost → render those at full fidelity.

**Revenue/EBITDA:** colo at a sober blended **$140–150/kW-mo** on ~70 MW net IT →
~$70M colo EBITDA; + byproducts (**45Q $23M is ~17% of EBITDA — material, not rounding**,
+ MISO ~$5–10M + heat/water) → **~$95–110M sober**. $132M needs **≥85–90 MW net IT or
premium ($180/kW-mo) pricing**.

**Project finance is internally inconsistent as stated.** DSCR 1.80x on $132M EBITDA
⇒ ~$73M max debt service ⇒ ~$777M debt @ ~7%/20yr = **only ~45% gearing** (below the
60–75% infra norm). The **"13-yr payback" = $1,720M/$132M = unlevered, pre-tax** — it
ignores debt and tax. Levered **equity payback ≈ 16–20 yr**. Present both; don't let
13 yr read as the equity return. Rebuild on the corrected **$2.0B / ~$100M** base.

**Top risks (likelihood × impact):** ① **45Q ineligibility** (binary cliff, −$23M →
DSCR <0.5x — the single point of failure); ② **fuel-supply scale** (one landfill
insufficient); ③ colo price/lease-up (−$15–30M); ④ SOFC degradation; ⑤ rates + capture
parasitic. DSCR 1.80x has ~$44M (33%) headroom to the 1.20x covenant — survives one
moderate shock, **breaks on 45Q loss or any two majors**.

**Site plan (~58 ha / ~143 acres total; greenhouse is ~63% of land).** Industrial core
is compact (~50 acres). Layout grid (origin SW, +X east, +Z north, meters) in `CONFIG.layout`.

---

## 6. The 3D model (Squad 6) — build plan

**Keep Three.js r128** (single-file, no-build constraint; r148 removes `examples/js`
globals → would force an ESM importmap rewrite for marginal gain).

**Highest-value robustness fix: vendor Three.js locally** (`vendor/three.min.js` +
`vendor/OrbitControls.js`) as the **first** entries in the CDN chain → works on GitHub
Pages with CDNs blocked (curl confirmed 403 here). `.nojekyll` already present.

**Single source of truth:** add a `CONFIG` object (1 unit = 1 m) so every geometry
dimension derives from the real numbers above; route all machines into one
`mkpCampus` group; replace magic literals with `CONFIG` reads.

**Performance:** convert repeated units (SOFC cabinets ×~230–300, immersion tanks,
coolers) to **InstancedMesh**; cache shared geometry/materials; clamp pixelRatio in the
resize handler; mobile detection; FPS guard. Target ≲150 draw calls.

**Geometry fixes (priority order):**
1. **SOFC farm** — replace 9 oversized gold boxes with **~230–300 instanced matte-gray
   cabinets (2.4 W × 2.9 H × 6 L)** in rows with an overhead pipe rack.
2. **Amine capture island** (missing) — **tall absorber (~2.5 r × 34 H, the site
   landmark)** + shorter stripper + horizontal reboiler + CO₂ compressor skid + well.
3. **Immersion data hall** — lower to **~10–12 m, squarer 80×80**, windowless.
4. **BESS** (missing) — white Megapack row / Megablock container.
5. **Dry-cooler field** (missing) — V-bank arrays with fan discs.
6. **Greenhouse** (missing) — large translucent glass slab (~360×360).
7. Water/brine tanks ≈ correct (16 m dia domes); add a brine/ZLD unit.

**Flows (animated):** make particle **speed & density ∝ flow magnitude** (not the
current uniform 0.004); use `getPointAt` (arc-length) for honest spacing. Color-code
streams; the **heat cascade must be one monotonic 800→180→85→50 °C chain that
terminates in a reject branch** (terminal leg does **not** wrap). Repurpose the legacy
flare embers as a cool **"methane destroyed" indicator** (gas is consumed, not flared).

**Labels & tour:** the 12-chapter data-driven tour is solid; wire its unused
`highlight` field to a pool of projected HTML `<div>` labels (cheaper/crisper than
CSS2DRenderer or sprite textures in single-file r128). Bind each chapter →
subsystem → **corrected headline number** (e.g. SOFC 53% LHV; net IT ~70 MW;
water +5,570 m³/day; captured ~325k t/yr; CapEx ~$2.0B).

---

## 7. CONFIG contract (model ↔ physics)

```js
// 1 unit = 1 metre. Every dimension below derives from §1–§6.
const CONFIG = {
  power:   { grossSOFC_MW:123, netIT_MW:70, eff_LHV:0.53, fuelUtil:0.85,
             fuel_MMBtu_h:620, fuel_scfm:20000 },
  bess:    { energy_MWh:20, power_MW:5, rtEff:0.92, units:4 /* Megablock */ },
  thermal: { sofcHeat_MW:40, itReject_MW:100, mdHeat_MW:20,
             greenhousePeak_MW:30, greenhouseAvg_MW:10, rejectWorstCase_MW:100,
             tiers_C:[700,200,85,50] /* monotonic; terminates at ambient */ },
  water:   { mdProduct_m3d:5500, combustion_m3d:520, netPositive_m3d:5570,
             requiresDryCooling:true, requiresMultiEffectMD:true },
  carbon:  { captured_tCO2_yr:325000, ch4Avoided_tCO2e_GWP100:2500000,
             embodied_tCO2e_yr:22000, carbonNegative:'GWP20+wideBoundary only',
             credit45Q_usd_yr:23000000 },
  finance: { capex_usd:2.0e9, ebitda_usd_yr:100e6, dscr:1.80,
             paybackUnlevered_yr:13, paybackEquity_yr:18, gearing:0.45 },
  geom: { // metres
    sofcModule:{w:2.4,h:2.9,d:6}, sofcCount:300, sofcRows:10,
    dataHall:{w:80,d:80,h:11},
    amineAbsorber:{r:2.5,h:34}, amineStripper:{r:2.0,h:18},
    bessUnit:{w:1.7,h:2.8,d:8.8}, bessCount:6,
    dryCoolerUnit:{l:12,h:4}, dryCoolerCount:14,
    greenhouse:{w:430,d:300,h:8},
    waterTank:{r:8,h:16}, tankCount:3
  },
  layout: { // metres, origin SW, +X east +Z north (Agent #25 site plan)
    substation:{x:40,z:40,w:90,d:80},   bess:{x:150,z:45,w:90,d:60},
    dryCoolers:{x:270,z:40,w:130,d:70},  dataHall:{x:270,z:130,w:110,d:85},
    gasCleanup:{x:420,z:40,w:60,d:40},   md:{x:500,z:40,w:50,d:40},
    sofc:{x:420,z:130,w:200,d:90},       amine:{x:420,z:240,w:120,d:100},
    greenhouse:{x:380,z:360,w:430,d:300}
  }
};
```

---

## Appendix — research lanes (30 agents, 6 squads)

1 SOFC electrochem · 2 fuel supply · 3 CHP heat · 4 BESS · 5 electrical BOP ·
6 immersion cooling · 7 IT load/PUE · 8 thermal cascade · 9 membrane distillation ·
10 heat rejection · 11 combustion water · 12 water balance · 13 effluent/brine ·
14 methane GWP · 15 aux water · 16 amine capture · 17 45Q · 18 lifecycle carbon ·
19 air permits · 20 greenhouse · 21 CapEx · 22 revenue/EBITDA · 23 DSCR/debt ·
24 sensitivity · 25 site layout · 26 scene architecture · 27 subsystem geometry ·
28 flow animation · 29 labels/tour · 30 perf/robustness.

*Every number above carries a sourced citation in the research record. Where lanes
disagreed (gross-vs-net MW, captured-CO₂ range, CapEx, EBITDA, heat contention), the
conference resolved to the conservative defensible value and flagged the assumption.*
