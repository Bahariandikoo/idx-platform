"""
IDX Trading Platform — Streamlit Dashboard
Run with: streamlit run dashboard/app.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf

from data.fetcher import DEFAULT_WATCHLIST, fetch_ticker, get_stock_info

UTAMA = ["AALI.JK", "ABMM.JK", "ACES.JK", "ADHI.JK", "AISA.JK", "AKRA.JK", "AMRT.JK", "ANTM.JK", "APLN.JK", "ARNA.JK", "ARTO.JK", "ASGR.JK", "ASII.JK", "ASRI.JK", "ASSA.JK", "AUTO.JK", "BACA.JK", "BALI.JK", "BAYU.JK", "BBCA.JK", "BBHI.JK", "BBNI.JK", "BBRI.JK", "BBTN.JK", "BBYB.JK", "BCAP.JK", "BDMN.JK", "BEST.JK", "BFIN.JK", "BGTG.JK", "BINA.JK", "BIRD.JK", "BISI.JK", "BJBR.JK", "BJTM.JK", "BKSL.JK", "BMRI.JK", "BMTR.JK", "BNGA.JK", "BNII.JK", "BNLI.JK", "BRMS.JK", "BRPT.JK", "BSDE.JK", "BSIM.JK", "BTPN.JK", "BUDI.JK", "BUKK.JK", "BUMI.JK", "BVIC.JK", "BWPT.JK", "BYAN.JK", "CASS.JK", "CFIN.JK", "CITA.JK", "CMNP.JK", "CPIN.JK", "CTRA.JK", "DEWA.JK", "DILD.JK", "DLTA.JK", "DMAS.JK", "DNET.JK", "DOID.JK", "DSNG.JK", "DSSA.JK", "ELSA.JK", "EMTK.JK", "ENRG.JK", "ERAA.JK", "ESSA.JK", "EXCL.JK", "GEMS.JK", "GGRM.JK", "GJTL.JK", "GWSA.JK", "HEXA.JK", "HMSP.JK", "HRUM.JK", "ICBP.JK", "IMAS.JK", "IMPC.JK", "INCO.JK", "INDF.JK", "INDY.JK", "INKP.JK", "INPC.JK", "INTP.JK", "ISAT.JK", "ISSP.JK", "ITMG.JK", "JKON.JK", "JPFA.JK", "JRPT.JK", "JSMR.JK", "JTPE.JK", "KBLI.JK", "KIJA.JK", "KKGI.JK", "KLBF.JK", "KPIG.JK", "LPKR.JK", "LPPF.JK", "LSIP.JK", "LTLS.JK", "MAIN.JK", "MAPI.JK", "MAYA.JK", "MBSS.JK", "MCOR.JK", "MDKA.JK", "MEDC.JK", "MEGA.JK", "MIDI.JK", "MIKA.JK", "MLBI.JK", "MLIA.JK", "MLPL.JK", "MMLP.JK", "MNCN.JK", "MPMX.JK", "MREI.JK", "MTDL.JK", "MTLA.JK", "MYOR.JK", "NISP.JK", "PANR.JK", "PANS.JK", "PGAS.JK", "PNBN.JK", "PNIN.JK", "PNLF.JK", "PTBA.JK", "PTPP.JK", "PTRO.JK", "PWON.JK", "RAJA.JK", "RALS.JK", "SAME.JK", "SCMA.JK", "SGRO.JK", "SIDO.JK", "SILO.JK", "SIMP.JK", "SMAR.JK", "SMBR.JK", "SMDR.JK", "SMGR.JK", "SMMA.JK", "SMRA.JK", "SMSM.JK", "SRTG.JK", "SSIA.JK", "SSMS.JK", "TBIG.JK", "TBLA.JK", "TINS.JK", "TKIM.JK", "TLKM.JK", "TMAS.JK", "TOBA.JK", "TOTL.JK", "TOWR.JK", "TPMA.JK", "TRIM.JK", "TSPC.JK", "ULTJ.JK", "UNIC.JK", "UNTR.JK", "UNVR.JK", "VICO.JK", "WIIM.JK", "WINS.JK", "WTON.JK", "SHIP.JK", "POWR.JK", "PRDA.JK", "BRIS.JK", "CARS.JK", "CLEO.JK", "WOOD.JK", "HRTA.JK", "MARK.JK", "MCAS.JK", "PSSI.JK", "MORA.JK", "PBID.JK", "IPCM.JK", "BTPS.JK", "SPTO.JK", "HEAL.JK", "TUGU.JK", "MSIN.JK", "MAPA.JK", "IPCC.JK", "FILM.JK", "PANI.JK", "GOOD.JK", "SKRN.JK", "BOLA.JK", "KEEN.JK", "TEBE.JK", "KEJU.JK", "PSGO.JK", "UCID.JK", "CSRA.JK", "SAMF.JK", "SGER.JK", "PNGO.JK", "BBSI.JK", "VICI.JK", "UNIQ.JK", "TAPG.JK", "BMHS.JK", "MCOL.JK", "GTSI.JK", "MTEL.JK", "CMRY.JK", "RMKE.JK", "AVIA.JK", "DRMA.JK", "ADMR.JK", "STAA.JK", "MTMH.JK", "TRGU.JK", "HATM.JK", "JARR.JK", "ELPI.JK", "MKTR.JK", "OMED.JK", "SUNI.JK", "PGEO.JK", "HILL.JK", "BDKR.JK", "CUAN.JK", "SMIL.JK", "AMMN.JK", "MAHA.JK", "ERAL.JK", "BREN.JK", "MSTI.JK", "GOLF.JK", "DAAZ.JK", "AADI.JK", "MDIY.JK", "DGWG.JK", "CBDK.JK", "MINE.JK", "PSAT.JK", "BLOG.JK", "YUPI.JK", "MDLA.JK", "NCKL.JK", "MBMA.JK", "RAAM.JK", "ADRO.JK", "AGRO.JK"]

PENGEMBANGAN = ["ACST.JK", "ADES.JK", "AKPI.JK", "AKSI.JK", "ALDO.JK", "ALKA.JK", "AMAG.JK", "AMFG.JK", "AMIN.JK", "ANJT.JK", "APEX.JK", "APIC.JK", "APII.JK", "APLI.JK", "ARGO.JK", "ARII.JK", "ARTA.JK", "ASBI.JK", "ASDM.JK", "ASJT.JK", "ASRM.JK", "ATIC.JK", "BABP.JK", "BAJA.JK", "BAPA.JK", "BBKP.JK", "BBLD.JK", "BBMD.JK", "BCIC.JK", "BCIP.JK", "BIPI.JK", "BKSW.JK", "BMAS.JK", "BMSR.JK", "BNBA.JK", "BOLT.JK", "BPFI.JK", "BPII.JK", "BRAM.JK", "BRNA.JK", "BSSR.JK", "BTON.JK", "BULL.JK", "BUVA.JK", "CEKA.JK", "CENT.JK", "CINT.JK", "CLPI.JK", "CPRO.JK", "CSAP.JK", "CTBN.JK", "CTTH.JK", "DART.JK", "DEFI.JK", "DGIK.JK", "DKFT.JK", "DNAR.JK", "DPNS.JK", "DSFI.JK", "DUTI.JK", "DVLA.JK", "DYAN.JK", "ECII.JK", "EKAD.JK", "EMDE.JK", "EPMT.JK", "ERTX.JK", "ESTI.JK", "FAST.JK", "FISH.JK", "FMII.JK", "FORU.JK", "FPNI.JK", "GDST.JK", "GDYR.JK", "GEMA.JK", "GMTD.JK", "GOLD.JK", "GPRA.JK", "GSMF.JK", "GTBO.JK", "GZCO.JK", "HDFA.JK", "HERO.JK", "IATA.JK", "IGAR.JK", "IKBI.JK", "IMJS.JK", "INAI.JK", "INCI.JK", "INDR.JK", "INDS.JK", "INDX.JK", "INPP.JK", "INRU.JK", "INTD.JK", "IPOL.JK", "ITMA.JK", "JAWA.JK", "JECC.JK", "JIHD.JK", "JSPT.JK", "KAEF.JK", "KBLM.JK", "KBLV.JK", "KDSI.JK", "KICI.JK", "KOBX.JK", "KONI.JK", "KOPI.JK", "KRAS.JK", "LAPD.JK", "LEAD.JK", "LINK.JK", "LION.JK", "LMPI.JK", "LPCK.JK", "LPGI.JK", "LPIN.JK", "LPLI.JK", "LPPS.JK", "LRNA.JK", "MBAP.JK", "MBTO.JK", "MDLN.JK", "MERK.JK", "MGNA.JK", "MICE.JK", "MITI.JK", "MKPI.JK", "MLPT.JK", "MPPA.JK", "MRAT.JK", "MSKY.JK", "MYOH.JK", "NELY.JK", "NIKL.JK", "NIRO.JK", "NOBU.JK", "NRCA.JK", "OKAS.JK", "PADI.JK", "PALM.JK", "PDES.JK", "PEGE.JK", "PGLI.JK", "PICO.JK", "PJAA.JK", "PKPK.JK", "PNBS.JK", "PNSE.JK", "PSAB.JK", "PSDN.JK", "PSKT.JK", "PTIS.JK", "PTSN.JK", "PTSP.JK", "PUDP.JK", "PYFA.JK", "RANC.JK", "RDTX.JK", "RELI.JK", "RIGS.JK", "ROTI.JK", "RUIS.JK", "SAFE.JK", "SCCO.JK", "SDMU.JK", "SDPC.JK", "SDRA.JK", "SHID.JK", "SKBM.JK", "SKLT.JK", "SMDM.JK", "SMMT.JK", "SOCI.JK", "SONA.JK", "SPMA.JK", "SRAJ.JK", "SRSN.JK", "SSTM.JK", "STAR.JK", "STTP.JK", "SULI.JK", "TALF.JK", "TBMS.JK", "TCID.JK", "TGKA.JK", "TIFA.JK", "TIRA.JK", "TMPO.JK", "TOTO.JK", "TPIA.JK", "TRIS.JK", "TRST.JK", "TRUS.JK", "UNIT.JK", "VINS.JK", "VOKS.JK", "VRNA.JK", "WAPO.JK", "WEHA.JK", "WOMF.JK", "YPAS.JK", "YULE.JK", "CASA.JK", "DAYA.JK", "DPUM.JK", "IDPR.JK", "KINO.JK", "OASA.JK", "PBSA.JK", "BOGA.JK", "PORT.JK", "MINA.JK", "CSIS.JK", "FIRE.JK", "KMTR.JK", "MAPB.JK", "HOKI.JK", "MPOW.JK", "MDKI.JK", "BELL.JK", "MTWI.JK", "PPRE.JK", "WEGE.JK", "DWGL.JK", "JMAS.JK", "CAMP.JK", "LCKM.JK", "HELI.JK", "GHON.JK", "DFAM.JK", "NICK.JK", "PRIM.JK", "TRUK.JK", "PZZA.JK", "TNCA.JK", "TCPI.JK", "RISE.JK", "BPTR.JK", "NFCX.JK", "MGRO.JK", "MOLI.JK", "CITY.JK", "SAPX.JK", "SURE.JK", "MPRO.JK", "CAKK.JK", "SATU.JK", "DIVA.JK", "LUCK.JK", "URBN.JK", "SOTS.JK", "ZONE.JK", "PEHA.JK", "BEEF.JK", "CLAY.JK", "NATO.JK", "JAYA.JK", "JAST.JK", "FITT.JK", "CCSI.JK", "SFAN.JK", "POLU.JK", "KJEN.JK", "ITIC.JK", "PAMG.JK", "BLUE.JK", "EAST.JK", "LIFE.JK", "FUJI.JK", "INOV.JK", "SMKL.JK", "HDIT.JK", "TFAS.JK", "GGRP.JK", "OPMS.JK", "NZIA.JK", "SLIS.JK", "IRRA.JK", "DMMX.JK", "WOWS.JK", "ESIP.JK", "AGAR.JK", "IFSH.JK", "REAL.JK", "IFII.JK", "PMJS.JK", "GLVA.JK", "AMAR.JK", "INDO.JK", "AMOR.JK", "TRIN.JK", "DMND.JK", "PTPW.JK", "IKAN.JK", "RONY.JK", "CSMI.JK", "BBSS.JK", "BHAT.JK", "UANG.JK", "PGUN.JK", "TRJA.JK", "SCNP.JK", "KMDS.JK", "PURI.JK", "SOHO.JK", "HOMI.JK", "ROCK.JK", "ATAP.JK", "BANK.JK", "EDGE.JK", "SNLK.JK", "ZYRX.JK", "NPGF.JK", "ADCP.JK", "HOPE.JK", "TRUE.JK", "LABA.JK", "ARCI.JK", "MASB.JK", "NICL.JK", "UVCR.JK", "HAIS.JK", "OILS.JK", "GPSO.JK", "SBMA.JK", "CMNT.JK", "KUAS.JK", "BOBA.JK", "DEPO.JK", "BINO.JK", "TAYS.JK", "OBMD.JK", "NASI.JK", "BSML.JK", "SEMA.JK", "ASLC.JK", "NETV.JK", "ENAK.JK", "NTBK.JK", "BIKE.JK", "WIRG.JK", "SICO.JK", "TLDN.JK", "ASHA.JK", "SWID.JK", "ARKO.JK", "CHEM.JK", "DEWI.JK", "AXIO.JK", "KRYA.JK", "GULA.JK", "TOOL.JK", "BUAH.JK", "CRAB.JK", "MEDS.JK", "COAL.JK", "PRAY.JK", "CBUT.JK", "BSBK.JK", "PDPP.JK", "KDTN.JK", "ZATA.JK", "MMIX.JK", "PADA.JK", "VTNY.JK", "ELIT.JK", "BEER.JK", "CBPE.JK", "CBRE.JK", "WINE.JK", "PEVE.JK", "LAJU.JK", "FWCT.JK", "IRSX.JK", "VAST.JK", "HALO.JK", "FUTR.JK", "PTMP.JK", "TRON.JK", "NSSS.JK", "GTRA.JK", "JATI.JK", "TYRE.JK", "MPXL.JK", "KLAS.JK", "MAXI.JK", "VKTR.JK", "CRSN.JK", "INET.JK", "CNMA.JK", "FOLK.JK", "GRIA.JK", "PPRI.JK", "CYBR.JK", "MUTU.JK", "HUMI.JK", "RSCH.JK", "BABY.JK", "IOTF.JK", "KOCI.JK", "PTPS.JK", "STRK.JK", "KOKA.JK", "RGAS.JK", "IKPM.JK", "AYAM.JK", "SURI.JK", "ASLI.JK", "GRPH.JK", "SMGA.JK", "UNTD.JK", "TOSK.JK", "MPIX.JK", "MKAP.JK", "LIVE.JK", "HYGN.JK", "BAIK.JK", "VISI.JK", "AREA.JK", "MHKI.JK", "ATLA.JK", "DATA.JK", "SOLA.JK", "BATR.JK", "PART.JK", "ISEA.JK", "BLES.JK", "GUNA.JK", "LABS.JK", "DOSS.JK", "NEST.JK", "VERN.JK", "BOAT.JK", "NAIK.JK", "KSIX.JK", "RATU.JK", "YOII.JK", "HGII.JK", "BRRC.JK", "OBAT.JK", "ASPR.JK", "COIN.JK", "CDIA.JK", "MERI.JK", "CHEK.JK", "PMUI.JK", "EMAS.JK", "PJHB.JK", "RLCO.JK", "SUPA.JK", "KAQI.JK", "FORE.JK", "DKHH.JK", "AYLS.JK", "DADA.JK", "ASPI.JK", "BESS.JK", "AMAN.JK", "CARE.JK", "PIPA.JK", "AWAN.JK", "DOOH.JK", "CGAS.JK", "NICE.JK", "MSJA.JK", "SMLE.JK", "ACRO.JK", "WIFI.JK", "FAPA.JK", "DCII.JK", "KETR.JK", "DGNS.JK", "UFOE.JK", "ADMF.JK", "ADMG.JK", "AGII.JK", "AGRS.JK", "AHAP.JK", "AIMS.JK"]

PEMANTAUAN_KHUSUS = ["ABBA.JK", "ABDA.JK", "AKKU.JK", "ALMI.JK", "ALTO.JK", "ARTI.JK", "ASMI.JK", "BATA.JK", "BBRM.JK", "BEKS.JK", "BHIT.JK", "BIKA.JK", "BIMA.JK", "BIPP.JK", "BKDP.JK", "BLTA.JK", "BLTZ.JK", "BNBR.JK", "BSWD.JK", "BTEK.JK", "BTEL.JK", "CANI.JK", "CMPP.JK", "CNKO.JK", "CNTX.JK", "COWL.JK", "ELTY.JK", "ETWA.JK", "FASW.JK", "GAMA.JK", "GIAA.JK", "GLOB.JK", "GOLL.JK", "HADE.JK", "HITS.JK", "HOME.JK", "HOTL.JK", "IBFN.JK", "IBST.JK", "ICON.JK", "IIKP.JK", "IKAI.JK", "INAF.JK", "INTA.JK", "KARW.JK", "KBRI.JK", "KIAS.JK", "KOIN.JK", "KREN.JK", "LCGP.JK", "LMAS.JK", "LMSH.JK", "MAGP.JK", "MDIA.JK", "MDRN.JK", "META.JK", "MFMI.JK", "MIRA.JK", "MTFN.JK", "MTSM.JK", "MYTX.JK", "OCAP.JK", "OMRE.JK", "PBRX.JK", "PLAS.JK", "PLIN.JK", "POLY.JK", "POOL.JK", "PPRO.JK", "RBMS.JK", "RICY.JK", "RIMO.JK", "RODA.JK", "SCPI.JK", "SIMA.JK", "SIPD.JK", "SKYB.JK", "SMCB.JK", "SMRU.JK", "SQMI.JK", "SRIL.JK", "SUGI.JK", "SUPR.JK", "TARA.JK", "TAXI.JK", "TELE.JK", "TFCO.JK", "TIRT.JK", "TRAM.JK", "TRIL.JK", "TRIO.JK", "UNSP.JK", "VIVA.JK", "WICO.JK", "WIKA.JK", "WSKT.JK", "ZBRA.JK", "JGLE.JK", "MARI.JK", "MKNT.JK", "MTRA.JK", "INCF.JK", "WSBP.JK", "TAMU.JK", "TGRA.JK", "TOPS.JK", "ARMY.JK", "MABA.JK", "NASA.JK", "KIOS.JK", "GMFI.JK", "ZINC.JK", "PCAR.JK", "BOSS.JK", "JSKY.JK", "INPS.JK", "TDPM.JK", "SWAT.JK", "POLL.JK", "NUSA.JK", "ANDI.JK", "LAND.JK", "DIGI.JK", "HKMU.JK", "DUCK.JK", "YELO.JK", "SOSS.JK", "DEAL.JK", "POLA.JK", "FOOD.JK", "POLI.JK", "COCO.JK", "MTPS.JK", "CPRI.JK", "HRME.JK", "POSA.JK", "KAYU.JK", "IPTV.JK", "ENVY.JK", "KOTA.JK", "ARKA.JK", "BAPI.JK", "PURE.JK", "SINI.JK", "PURA.JK", "TAMA.JK", "SBAT.JK", "KBAG.JK", "CBMF.JK", "TECH.JK", "EPAC.JK", "TOYS.JK", "ENZO.JK", "PTDU.JK", "PMMP.JK", "WMUU.JK", "BEBS.JK", "FIMP.JK", "MGLV.JK", "RSGK.JK", "WMPP.JK", "IPPE.JK", "BAUT.JK", "WINR.JK", "RAFI.JK", "KKES.JK", "SAGE.JK", "TGUK.JK", "RMKO.JK", "ALII.JK", "PTMR.JK", "ESTA.JK"]

AKSELERASI = ["PGJO.JK", "CASH.JK", "SOFA.JK", "PPGL.JK", "PLAN.JK", "LFLO.JK", "LUCY.JK", "IPAC.JK", "FLMC.JK", "RUNS.JK", "IDEA.JK", "WGSH.JK", "SMKM.JK", "NANO.JK", "IBOS.JK", "OLIV.JK", "RCCC.JK", "AMMS.JK", "EURO.JK", "KLIN.JK", "NINE.JK", "ISAP.JK", "SOUL.JK", "BMBL.JK", "NAYZ.JK", "PACK.JK", "CHIP.JK", "KING.JK", "HAJJ.JK", "RELF.JK", "GRPM.JK", "WIDI.JK", "HBAT.JK", "LMAX.JK", "MSIE.JK", "AEGS.JK", "LOPI.JK", "UDNG.JK", "MEJA.JK", "SPRE.JK", "MENN.JK", "MANG.JK"]

ALL_IDX_STOCKS = UTAMA + PENGEMBANGAN + PEMANTAUAN_KHUSUS + AKSELERASI
from indicators.indicators import add_all_indicators
from backtester.engine import (
    run_backtest,
    rsi_strategy,
    macd_crossover_strategy,
    ema_crossover_strategy,
    ema_9_21_strategy,
)

# ─── PAGE CONFIG ────────────────────────────────────────────────────

st.set_page_config(
    page_title="IDX Stonks Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Syne', sans-serif;
    }
    .stApp {
        background: #0a0e1a;
        color: #e8eaf0;
    }
    .main-title {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 2.4rem;
        background: linear-gradient(135deg, #00d4aa, #00a8ff, #7c5fe6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }
    .metric-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 4px 0;
    }
    .ticker-badge {
        background: linear-gradient(135deg, #00d4aa22, #00a8ff22);
        border: 1px solid #00d4aa44;
        border-radius: 8px;
        padding: 4px 12px;
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
        color: #00d4aa;
    }
    [data-testid="stSidebar"] {
        background: #0d1117 !important;
        border-right: 1px solid #1f2937;
    }
    .stSelectbox > div > div {
        background: #111827;
        border: 1px solid #1f2937;
        color: #e8eaf0;
    }
    div[data-testid="metric-container"] {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 12px 16px;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Space Mono', monospace;
        font-size: 0.8rem;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# ─── HELPERS ────────────────────────────────────────────────────────

@st.cache_data(ttl=900)  # Cache 15 min
def load_data(ticker: str, period: str, interval: str = "1d") -> pd.DataFrame:
    df = fetch_ticker(ticker, period=period, interval=interval)
    if df.empty:
        return df
    return add_all_indicators(df)


@st.cache_data(ttl=3600)
def load_info(ticker: str) -> dict:
    return get_stock_info(ticker)


def color_metric(val, good_above=0):
    return "🟢" if val > good_above else "🔴"


# ─── SIDEBAR ────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 📈 IDX Platform")
    st.markdown("---")

    # Ticker selector
    custom = st.text_input("Custom ticker (e.g. BBCA.JK)", "")
    
    board_filter = st.selectbox("Filter Papan", 
        ["Default Watchlist", "Utama (257)", "Pengembangan (482)", "Pemantauan Khusus (172)", "Akselerasi (42)", "Semua (953)"],
        index=0
    )
    board_map = {
        "Default Watchlist": DEFAULT_WATCHLIST,
        "Utama (257)": UTAMA,
        "Pengembangan (482)": PENGEMBANGAN,
        "Pemantauan Khusus (172)": PEMANTAUAN_KHUSUS,
        "Akselerasi (42)": AKSELERASI,
        "Semua (953)": ALL_IDX_STOCKS,
    }
    watchlist = board_map[board_filter].copy()
    if custom and not custom.endswith(".JK"):
        custom = custom.upper() + ".JK"
    if custom:
        watchlist.insert(0, custom.upper())

    selected_ticker = st.selectbox("Select Stock", watchlist, index=0)

    timeframe = st.selectbox(
        "Candle Timeframe",
        ["1d", "1wk", "1h", "30m", "15m"],
        index=0,
        help="Intraday timeframes (1h, 30m, 15m) only support up to ~60 days of data"
    )

    period = st.select_slider(
        "Data Period",
        options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        value="1y"
    )

    # Warn user about intraday limits
    if timeframe in ["1h", "30m", "15m"] and period not in ["1mo", "3mo"]:
        st.warning("⚠️ Intraday data only available for up to 60 days. Switch period to 1mo or 3mo.")

    st.markdown("---")
    st.markdown("**Indicators**")
    show_ema20 = st.checkbox("EMA 20", value=True)
    show_ema50 = st.checkbox("EMA 50", value=True)
    show_sma200 = st.checkbox("SMA 200", value=False)
    show_bb = st.checkbox("Bollinger Bands", value=False)
    show_vwap = st.checkbox("VWAP", value=False)

    st.markdown("---")
    st.caption("🕐 Data refreshes every 15 min")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()


# ─── MAIN CONTENT ───────────────────────────────────────────────────

st.markdown('<div class="main-title">IDX Stonks Platform 🚀</div>', unsafe_allow_html=True)
st.caption(f"Bursa Efek Indonesia · Personal Trading Dashboard")
st.markdown("")

# Load data
with st.spinner(f"Loading {selected_ticker}..."):
    df = load_data(selected_ticker, period, timeframe)
    info = load_info(selected_ticker)

if df.empty:
    st.error(f"❌ Could not fetch data for **{selected_ticker}**. Check the ticker and try again.")
    st.stop()

latest = df.iloc[-1]
prev = df.iloc[-2]
price_change = latest["close"] - prev["close"]
price_change_pct = price_change / prev["close"] * 100

# ─── TOP METRICS ────────────────────────────────────────────────────

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(
        label=f"**{selected_ticker}**",
        value=f"Rp {latest['close']:,.0f}",
        delta=f"{price_change_pct:+.2f}%"
    )
with col2:
    st.metric("RSI (14)", f"{latest['rsi']:.1f}",
              delta="Oversold" if latest['rsi'] < 30 else ("Overbought" if latest['rsi'] > 70 else "Neutral"))
with col3:
    st.metric("MACD", f"{latest['macd']:.2f}",
              delta=f"Hist: {latest['macd_hist']:+.2f}")
with col4:
    st.metric("Momentum Score", f"{latest['momentum_score']:.0f}/100")
with col5:
    st.metric("Volume", f"{latest['volume']:,.0f}")
with col6:
    pe = info.get("pe_ratio", "N/A")
    st.metric("P/E Ratio", f"{pe:.1f}" if isinstance(pe, float) else pe)

st.markdown(f"""
**{info.get('name', selected_ticker)}** · {info.get('sector', '')} · {info.get('industry', '')}
""")

# Show active timeframe
st.caption(f"📊 Timeframe: `{timeframe}` · Period: `{period}`")
st.markdown("---")

# ─── TABS ────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs(["📊 Chart & Indicators", "⚙️ Backtesting", "🔍 Screener", "🏆 Multi-Stock Backtest"])


# ════════════════════════════════════════════
# TAB 1: CHART
# ════════════════════════════════════════════
with tab1:
    rows = 4
    row_heights = [0.55, 0.15, 0.15, 0.15]
    subplot_titles = ["Price", "Volume", "RSI (14)", "MACD"]

    fig = make_subplots(
        rows=rows, cols=1,
        shared_xaxes=True,
        row_heights=row_heights,
        subplot_titles=subplot_titles,
        vertical_spacing=0.04
    )

    # — Candlestick
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["open"], high=df["high"],
        low=df["low"], close=df["close"],
        name="Price",
        increasing_line_color="#00d4aa",
        decreasing_line_color="#ff4d6d",
        increasing_fillcolor="rgba(0,212,170,0.2)",
        decreasing_fillcolor="rgba(255,77,109,0.2)",
    ), row=1, col=1)

    # — Overlays
    if show_ema20:
        fig.add_trace(go.Scatter(x=df.index, y=df["ema_20"], name="EMA 20",
                                  line=dict(color="#00a8ff", width=1.5), opacity=0.9), row=1, col=1)
    if show_ema50:
        fig.add_trace(go.Scatter(x=df.index, y=df["ema_50"], name="EMA 50",
                                  line=dict(color="#f59e0b", width=1.5), opacity=0.9), row=1, col=1)
    if show_sma200:
        fig.add_trace(go.Scatter(x=df.index, y=df["sma_200"], name="SMA 200",
                                  line=dict(color="#a78bfa", width=1.5, dash="dash"), opacity=0.8), row=1, col=1)
    if show_bb:
        fig.add_trace(go.Scatter(x=df.index, y=df["bb_upper"], name="BB Upper",
                                  line=dict(color="#94a3b8", width=1, dash="dot"), opacity=0.6), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df["bb_lower"], name="BB Lower",
                                  line=dict(color="#94a3b8", width=1, dash="dot"),
                                  fill="tonexty", fillcolor="rgba(148,163,184,0.05)", opacity=0.6), row=1, col=1)
    if show_vwap:
        fig.add_trace(go.Scatter(x=df.index, y=df["vwap"], name="VWAP",
                                  line=dict(color="#f97316", width=1.5, dash="dash"), opacity=0.8), row=1, col=1)

    # — Volume bars
    colors = ["#00d4aa" if c >= o else "#ff4d6d" for c, o in zip(df["close"], df["open"])]
    fig.add_trace(go.Bar(x=df.index, y=df["volume"], name="Volume",
                          marker_color=colors, opacity=0.7), row=2, col=1)

    # — RSI
    fig.add_trace(go.Scatter(x=df.index, y=df["rsi"], name="RSI",
                              line=dict(color="#a78bfa", width=2)), row=3, col=1)
    fig.add_hline(y=70, line_dash="dot", line_color="#ff4d6d", opacity=0.5, row=3, col=1)
    fig.add_hline(y=30, line_dash="dot", line_color="#00d4aa", opacity=0.5, row=3, col=1)

    # — MACD
    hist_colors = ["#00d4aa" if v >= 0 else "#ff4d6d" for v in df["macd_hist"]]
    fig.add_trace(go.Bar(x=df.index, y=df["macd_hist"], name="MACD Hist",
                          marker_color=hist_colors, opacity=0.7), row=4, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["macd"], name="MACD",
                              line=dict(color="#00a8ff", width=1.5)), row=4, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["macd_signal"], name="Signal",
                              line=dict(color="#f59e0b", width=1.5)), row=4, col=1)

    fig.update_layout(
        height=750,
        paper_bgcolor="#0a0e1a",
        plot_bgcolor="#0d1117",
        font=dict(family="Space Mono", color="#94a3b8", size=11),
        legend=dict(bgcolor="#0d1117", bordercolor="#1f2937", borderwidth=1,
                     font=dict(size=10)),
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=30, b=10),
        showlegend=True,
    )
    for i in range(1, rows + 1):
        fig.update_yaxes(
            gridcolor="#1f2937", gridwidth=0.5,
            zerolinecolor="#374151",
            row=i, col=1
        )
        fig.update_xaxes(
            gridcolor="#1f2937", gridwidth=0.5,
            row=i, col=1
        )

    st.plotly_chart(fig, use_container_width=True)

    # Signal summary
    st.markdown("#### 📡 Current Signal Summary")
    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        rsi_v = latest["rsi"]
        rsi_sig = "🟢 Oversold" if rsi_v < 30 else ("🔴 Overbought" if rsi_v > 70 else "⚪ Neutral")
        st.info(f"**RSI Signal**\n\n{rsi_sig} ({rsi_v:.1f})")
    with sc2:
        macd_sig = "🟢 Bullish" if latest["macd_hist"] > 0 else "🔴 Bearish"
        st.info(f"**MACD Signal**\n\n{macd_sig}")
    with sc3:
        ema_sig = "🟢 Above EMA20" if latest["close"] > latest["ema_20"] else "🔴 Below EMA20"
        st.info(f"**Trend (EMA20)**\n\n{ema_sig}")
    with sc4:
        ms = latest["momentum_score"]
        ms_sig = "🟢 Bullish" if ms > 20 else ("🔴 Bearish" if ms < -20 else "⚪ Neutral")
        st.info(f"**Momentum Score**\n\n{ms_sig} ({ms:.0f})")


# ════════════════════════════════════════════
# TAB 2: BACKTESTING
# ════════════════════════════════════════════
with tab2:
    st.markdown("### ⚙️ Strategy Backtester")
    st.caption(f"Running on `{timeframe}` candles · {period} of data — change timeframe in the sidebar")

    bc1, bc2, bc3, bc4 = st.columns(4)
    with bc1:
        strategy_name = st.selectbox("Strategy", [
            "RSI Oversold/Overbought",
            "MACD Crossover",
            "EMA Crossover (20/50)",
            "EMA 9/21 Crossover",
        ])
    with bc2:
        capital = st.number_input("Initial Capital (IDR)", min_value=1_000_000,
                                   max_value=1_000_000_000, value=10_000_000, step=1_000_000,
                                   format="%d")
    with bc3:
        if strategy_name == "RSI Oversold/Overbought":
            oversold = st.slider("Oversold threshold", 20, 45, 30)
            signal_fn = lambda d: rsi_strategy(d, oversold, overbought if 'overbought' in dir() else 70)
        elif strategy_name == "MACD Crossover":
            st.markdown("&nbsp;")
            signal_fn = macd_crossover_strategy
        elif strategy_name == "EMA 9/21 Crossover":
            st.info("📌 EMA 9 > EMA 21 → BUY\nEMA 9 < EMA 21 → SELL")
            signal_fn = ema_9_21_strategy
        else:
            fast = st.slider("Fast EMA", 5, 50, 20)
            signal_fn = lambda d: ema_crossover_strategy(d, fast, slow if 'slow' in dir() else 50)
    with bc4:
        if strategy_name == "RSI Oversold/Overbought":
            overbought = st.slider("Overbought threshold", 55, 85, 70)
            signal_fn = lambda d: rsi_strategy(d, oversold, overbought)
        elif strategy_name == "MACD Crossover":
            st.markdown("&nbsp;")
        elif strategy_name == "EMA 9/21 Crossover":
            st.markdown("&nbsp;")
        else:
            slow = st.slider("Slow EMA", 20, 200, 50)
            signal_fn = lambda d: ema_crossover_strategy(d, fast, slow)

    run_btn = st.button("▶ Run Backtest", use_container_width=True, type="primary")

    if run_btn:
        with st.spinner("Running backtest..."):
            result = run_backtest(df, signal_fn, initial_capital=capital)
            summary = result.summary()

            # Build signal series for chart (shifted same as engine)
            raw_signals = signal_fn(df).shift(1).fillna(0)
            buy_signals  = df[raw_signals == 1]
            sell_signals = df[raw_signals == -1]

        # ── Summary metrics ──────────────────────────────────────
        st.markdown("#### 📊 Results")
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("Total Return",      f"{summary['Total Return (%)']:+.2f}%")
        m2.metric("Win Rate",          f"{summary['Win Rate (%)']:.1f}%")
        m3.metric("Sharpe Ratio",      f"{summary['Sharpe Ratio']:.2f}")
        m4.metric("Total Trades",      summary["Total Trades"])
        m5.metric("Max Drawdown",      f"{summary['Max Drawdown (%)']:.2f}%")
        m6.metric("Avg Return/Trade",  f"{summary['Avg Return/Trade (%)']:+.2f}%")

        st.markdown("---")

        # ── Strategy Chart with signals ──────────────────────────
        st.markdown("#### 📈 Strategy Chart")

        # Decide which indicator subplots to show based on strategy
        if strategy_name == "RSI Oversold/Overbought":
            bt_rows = 3
            bt_heights = [0.60, 0.20, 0.20]
            bt_titles = ["Price + Buy/Sell Signals", "Volume", "RSI (14)"]
        elif strategy_name == "MACD Crossover":
            bt_rows = 3
            bt_heights = [0.60, 0.20, 0.20]
            bt_titles = ["Price + Buy/Sell Signals", "Volume", "MACD"]
        else:  # EMA Crossover
            bt_rows = 2
            bt_heights = [0.75, 0.25]
            bt_titles = ["Price + Buy/Sell Signals", "Volume"]

        fig_bt = make_subplots(
            rows=bt_rows, cols=1,
            shared_xaxes=True,
            row_heights=bt_heights,
            subplot_titles=bt_titles,
            vertical_spacing=0.05,
        )

        # Candlestick
        fig_bt.add_trace(go.Candlestick(
            x=df.index,
            open=df["open"], high=df["high"],
            low=df["low"], close=df["close"],
            name="Price",
            increasing_line_color="#00d4aa",
            decreasing_line_color="#ff4d6d",
            increasing_fillcolor="rgba(0,212,170,0.2)",
            decreasing_fillcolor="rgba(255,77,109,0.2)",
        ), row=1, col=1)

        # Strategy-specific overlays on price chart
        if strategy_name in ("EMA Crossover (20/50)", "EMA 9/21 Crossover"):
            ema_fast_val = 9  if strategy_name == "EMA 9/21 Crossover" else fast
            ema_slow_val = 21 if strategy_name == "EMA 9/21 Crossover" else slow
            from indicators.indicators import ema as calc_ema
            fig_bt.add_trace(go.Scatter(
                x=df.index, y=calc_ema(df, ema_fast_val), name=f"EMA {ema_fast_val}",
                line=dict(color="#00a8ff", width=1.5), opacity=0.9
            ), row=1, col=1)
            fig_bt.add_trace(go.Scatter(
                x=df.index, y=calc_ema(df, ema_slow_val), name=f"EMA {ema_slow_val}",
                line=dict(color="#f59e0b", width=1.5), opacity=0.9
            ), row=1, col=1)

        # ── BUY signals — green triangles pointing UP ──
        fig_bt.add_trace(go.Scatter(
            x=buy_signals.index,
            y=buy_signals["low"] * 0.985,  # slightly below candle low
            mode="markers+text",
            marker=dict(symbol="triangle-up", size=14, color="#00d4aa",
                        line=dict(color="#00d4aa", width=1)),
            text=["BUY"] * len(buy_signals),
            textposition="bottom center",
            textfont=dict(size=9, color="#00d4aa", family="Space Mono"),
            name="BUY Signal",
        ), row=1, col=1)

        # ── SELL signals — red triangles pointing DOWN ──
        fig_bt.add_trace(go.Scatter(
            x=sell_signals.index,
            y=sell_signals["high"] * 1.015,  # slightly above candle high
            mode="markers+text",
            marker=dict(symbol="triangle-down", size=14, color="#ff4d6d",
                        line=dict(color="#ff4d6d", width=1)),
            text=["SELL"] * len(sell_signals),
            textposition="top center",
            textfont=dict(size=9, color="#ff4d6d", family="Space Mono"),
            name="SELL Signal",
        ), row=1, col=1)

        # Draw entry→exit lines for each trade
        for trade in result.trades:
            fig_bt.add_shape(
                type="line",
                x0=trade.entry_date, x1=trade.exit_date,
                y0=trade.entry_price, y1=trade.exit_price,
                line=dict(
                    color="#00d4aa" if trade.pnl >= 0 else "#ff4d6d",
                    width=1, dash="dot"
                ),
                row=1, col=1
            )

        # Volume
        vol_colors = ["#00d4aa" if c >= o else "#ff4d6d"
                      for c, o in zip(df["close"], df["open"])]
        fig_bt.add_trace(go.Bar(
            x=df.index, y=df["volume"], name="Volume",
            marker_color=vol_colors, opacity=0.6
        ), row=2, col=1)

        # Strategy indicator subplot
        if strategy_name == "RSI Oversold/Overbought":
            fig_bt.add_trace(go.Scatter(
                x=df.index, y=df["rsi"], name="RSI",
                line=dict(color="#a78bfa", width=2)
            ), row=3, col=1)
            fig_bt.add_hline(y=overbought, line_dash="dot", line_color="#ff4d6d",
                              opacity=0.7, row=3, col=1)
            fig_bt.add_hline(y=oversold,   line_dash="dot", line_color="#00d4aa",
                              opacity=0.7, row=3, col=1)
            # Shade oversold/overbought zones
            fig_bt.add_hrect(y0=0,          y1=oversold,   fillcolor="rgba(0,212,170,0.05)",
                              line_width=0, row=3, col=1)
            fig_bt.add_hrect(y0=overbought, y1=100,        fillcolor="rgba(255,77,109,0.05)",
                              line_width=0, row=3, col=1)

        elif strategy_name == "MACD Crossover":
            hist_colors = ["#00d4aa" if v >= 0 else "#ff4d6d" for v in df["macd_hist"]]
            fig_bt.add_trace(go.Bar(
                x=df.index, y=df["macd_hist"], name="MACD Hist",
                marker_color=hist_colors, opacity=0.7
            ), row=3, col=1)
            fig_bt.add_trace(go.Scatter(
                x=df.index, y=df["macd"], name="MACD",
                line=dict(color="#00a8ff", width=1.5)
            ), row=3, col=1)
            fig_bt.add_trace(go.Scatter(
                x=df.index, y=df["macd_signal"], name="Signal",
                line=dict(color="#f59e0b", width=1.5)
            ), row=3, col=1)

        fig_bt.update_layout(
            height=650,
            paper_bgcolor="#0a0e1a",
            plot_bgcolor="#0d1117",
            font=dict(family="Space Mono", color="#94a3b8", size=11),
            legend=dict(bgcolor="#0d1117", bordercolor="#1f2937", borderwidth=1,
                         font=dict(size=10)),
            xaxis_rangeslider_visible=False,
            margin=dict(l=10, r=10, t=30, b=10),
        )
        for i in range(1, bt_rows + 1):
            fig_bt.update_yaxes(gridcolor="#1f2937", zerolinecolor="#374151", row=i, col=1)
            fig_bt.update_xaxes(gridcolor="#1f2937", row=i, col=1)

        st.plotly_chart(fig_bt, use_container_width=True)

        # ── Equity curve ─────────────────────────────────────────
        st.markdown("#### 💰 Equity Curve")
        fig_eq = go.Figure()
        fig_eq.add_trace(go.Scatter(
            x=result.equity_curve.index,
            y=result.equity_curve,
            fill="tozeroy",
            fillcolor="rgba(0,212,170,0.08)",
            line=dict(color="#00d4aa", width=2),
            name="Portfolio Value"
        ))
        # Mark trade entries on equity curve
        for trade in result.trades:
            color = "#00d4aa" if trade.pnl >= 0 else "#ff4d6d"
            fig_eq.add_vline(x=trade.exit_date, line_dash="dot",
                              line_color=color, opacity=0.3)
        fig_eq.update_layout(
            paper_bgcolor="#0a0e1a", plot_bgcolor="#0d1117",
            font=dict(family="Space Mono", color="#94a3b8"),
            height=250,
            yaxis=dict(gridcolor="#1f2937", tickformat=",.0f"),
            xaxis=dict(gridcolor="#1f2937"),
            margin=dict(l=10, r=10, t=20, b=10),
            showlegend=False,
        )
        st.plotly_chart(fig_eq, use_container_width=True)

        # ── Trade log ────────────────────────────────────────────
        if result.trades:
            st.markdown("#### 📋 Trade Log")
            trades_df = pd.DataFrame([{
                "Entry Date":   t.entry_date,
                "Exit Date":    t.exit_date,
                "Entry Price":  f"Rp {t.entry_price:,.0f}",
                "Exit Price":   f"Rp {t.exit_price:,.0f}",
                "Shares":       t.shares,
                "P&L":          f"Rp {t.pnl:,.0f}",
                "Return %":     f"{t.pnl_pct:+.2f}%",
                "Result":       "✅ Win" if t.pnl > 0 else "❌ Loss",
            } for t in result.trades])
            st.dataframe(trades_df, use_container_width=True, height=280)
        else:
            st.warning("No trades were executed. Try adjusting the strategy parameters or period.")

    else:
        st.info("👆 Configure your strategy above and click **▶ Run Backtest**")


# ════════════════════════════════════════════
# TAB 3: SCREENER
# ════════════════════════════════════════════
with tab3:
    st.markdown("### 🔍 IDX Stock Screener")
    st.caption("Scan your watchlist for stocks matching technical criteria")

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        rsi_range = st.slider("RSI Range", 0, 100, (0, 100))
    with fc2:
        min_momentum = st.slider("Min Momentum Score", -100, 100, -100)
    with fc3:
        require_above_ema = st.checkbox("Must be above EMA 20")
        require_macd_bull = st.checkbox("Must have bullish MACD")

    custom_tickers = st.text_input(
        "Custom tickers to scan (comma-separated, e.g. BBCA.JK,TLKM.JK)",
        placeholder="Leave blank to use default watchlist"
    )

    if st.button("🔍 Run Screener", use_container_width=True, type="primary"):
        tickers_to_scan = ALL_IDX_STOCKS
        if custom_tickers:
            tickers_to_scan = [t.strip().upper() for t in custom_tickers.split(",")]
            tickers_to_scan = [t if t.endswith(".JK") else t + ".JK" for t in tickers_to_scan]

        with st.spinner(f"Scanning {len(tickers_to_scan)} stocks..."):
            from screener.screener import screen_stocks
            screen_df = screen_stocks(
                tickers=tickers_to_scan,
                rsi_min=rsi_range[0],
                rsi_max=rsi_range[1],
                min_momentum_score=min_momentum,
                require_above_ema20=require_above_ema,
                require_macd_bullish=require_macd_bull,
            )

        if screen_df.empty:
            st.warning("No stocks matched your criteria. Try relaxing the filters.")
        else:
            st.success(f"✅ Found **{len(screen_df)}** matching stocks")
            st.dataframe(
                screen_df.style.background_gradient(subset=["Momentum Score"], cmap="RdYlGn"),
                use_container_width=True
            )



# ════════════════════════════════════════════
# TAB 4: MULTI-STOCK BACKTEST
# ════════════════════════════════════════════
with tab4:
    st.markdown("### 🏆 Multi-Stock Backtest")
    st.caption("Jalanin satu strategy ke semua saham sekaligus — lihat winrate & return per emiten")

    # ── Config row ──────────────────────────────────────────────────
    mb1, mb2, mb3, mb4 = st.columns(4)
    with mb1:
        ms_strategy = st.selectbox("Strategy", [
            "EMA 9/21 Crossover",
            "MACD Crossover",
            "RSI Oversold/Overbought",
            "EMA Crossover (20/50)",
        ], key="ms_strategy")
    with mb2:
        ms_period = st.select_slider("Period", options=["1mo","3mo","6mo","1y","2y"], value="1y", key="ms_period")
        ms_tf = st.selectbox("Timeframe", ["1d","1wk"], index=0, key="ms_tf")
    with mb3:
        ms_capital = st.number_input("Capital per Saham (IDR)", min_value=1_000_000,
                                      max_value=100_000_000, value=10_000_000,
                                      step=1_000_000, format="%d", key="ms_capital")
        if ms_strategy == "RSI Oversold/Overbought":
            ms_oversold  = st.slider("Oversold",  20, 45, 30, key="ms_os")
            ms_overbought= st.slider("Overbought",55, 85, 70, key="ms_ob")
        elif ms_strategy == "EMA Crossover (20/50)":
            ms_fast = st.slider("Fast EMA", 5, 50, 20, key="ms_fast")
            ms_slow = st.slider("Slow EMA", 20, 200, 50, key="ms_slow")
    with mb4:
        ms_board = st.selectbox("Pilih Papan Saham", [
            "Default Watchlist (10 saham)",
            "Utama (257 saham)",
            "Pengembangan (482 saham)",
            "Pemantauan Khusus (172 saham)",
            "Akselerasi (42 saham)",
            "Semua IDX (953 saham) ⚠️ Lambat",
        ], key="ms_board")

        board_preset_map = {
            "Default Watchlist (10 saham)": DEFAULT_WATCHLIST,
            "Utama (257 saham)": UTAMA,
            "Pengembangan (482 saham)": PENGEMBANGAN,
            "Pemantauan Khusus (172 saham)": PEMANTAUAN_KHUSUS,
            "Akselerasi (42 saham)": AKSELERASI,
            "Semua IDX (953 saham) ⚠️ Lambat": ALL_IDX_STOCKS,
        }
        tickers_ms = board_preset_map[ms_board]
        st.caption(f"📋 {len(tickers_ms)} saham akan dibacktest")

    run_ms = st.button("▶ Jalankan Multi-Stock Backtest", use_container_width=True,
                        type="primary", key="run_ms")

    if run_ms:

        # Build signal function
        if ms_strategy == "EMA 9/21 Crossover":
            ms_signal_fn = ema_9_21_strategy
        elif ms_strategy == "MACD Crossover":
            ms_signal_fn = macd_crossover_strategy
        elif ms_strategy == "RSI Oversold/Overbought":
            ms_signal_fn = lambda d: rsi_strategy(d, ms_oversold, ms_overbought)
        else:
            ms_signal_fn = lambda d: ema_crossover_strategy(d, ms_fast, ms_slow)

        rows = []
        progress = st.progress(0, text="Starting...")
        status   = st.empty()

        for idx, ticker in enumerate(tickers_ms):
            progress.progress((idx) / len(tickers_ms), text=f"Processing {ticker}...")
            status.caption(f"⏳ {idx+1}/{len(tickers_ms)} — {ticker}")

            try:
                tdf = fetch_ticker(ticker, period=ms_period, interval=ms_tf)
                if tdf.empty or len(tdf) < 30:
                    rows.append({
                        "Ticker": ticker, "Status": "⚠️ No data",
                        "Trades": 0, "Win Rate %": "-", "Total Return %": "-",
                        "Max Drawdown %": "-", "Sharpe": "-", "Avg Return/Trade %": "-",
                        "Best Trade %": "-", "Worst Trade %": "-",
                    })
                    continue

                tdf = add_all_indicators(tdf)
                result = run_backtest(tdf, ms_signal_fn, initial_capital=ms_capital)
                s = result.summary()

                if result.trades:
                    best  = max(t.pnl_pct for t in result.trades)
                    worst = min(t.pnl_pct for t in result.trades)
                else:
                    best = worst = 0

                rows.append({
                    "Ticker":             ticker,
                    "Status":             "✅",
                    "Trades":             s["Total Trades"],
                    "Win Rate %":         s["Win Rate (%)"],
                    "Total Return %":     s["Total Return (%)"],
                    "Max Drawdown %":     s["Max Drawdown (%)"],
                    "Sharpe":             s["Sharpe Ratio"],
                    "Avg Return/Trade %": s["Avg Return/Trade (%)"],
                    "Best Trade %":       round(best, 2),
                    "Worst Trade %":      round(worst, 2),
                })

            except Exception as e:
                rows.append({
                    "Ticker": ticker, "Status": f"❌ {str(e)[:30]}",
                    "Trades": 0, "Win Rate %": "-", "Total Return %": "-",
                    "Max Drawdown %": "-", "Sharpe": "-", "Avg Return/Trade %": "-",
                    "Best Trade %": "-", "Worst Trade %": "-",
                })

        progress.progress(1.0, text="Done!")
        status.empty()

        result_df = pd.DataFrame(rows)

        # ── Summary stats across all stocks ─────────────────────
        valid = result_df[result_df["Status"] == "✅"].copy()

        if not valid.empty:
            st.markdown("#### 📊 Overall Summary")
            os1, os2, os3, os4, os5 = st.columns(5)
            avg_wr  = valid["Win Rate %"].mean()
            avg_ret = valid["Total Return %"].mean()
            avg_sh  = valid["Sharpe"].mean()
            best_stock  = valid.loc[valid["Total Return %"].idxmax(), "Ticker"]
            worst_stock = valid.loc[valid["Total Return %"].idxmin(), "Ticker"]

            os1.metric("Avg Win Rate",    f"{avg_wr:.1f}%")
            os2.metric("Avg Total Return",f"{avg_ret:+.2f}%")
            os3.metric("Avg Sharpe",      f"{avg_sh:.2f}")
            os4.metric("🏆 Best Stock",   best_stock)
            os5.metric("💀 Worst Stock",  worst_stock)

            st.markdown("---")

            # ── Win Rate bar chart ───────────────────────────────
            st.markdown("#### 📈 Win Rate per Emiten")
            sorted_wr = valid.sort_values("Win Rate %", ascending=False)
            bar_colors = ["#00d4aa" if w >= 50 else "#ff4d6d"
                          for w in sorted_wr["Win Rate %"]]
            fig_wr = go.Figure(go.Bar(
                x=sorted_wr["Ticker"],
                y=sorted_wr["Win Rate %"],
                marker_color=bar_colors,
                text=[f"{w:.0f}%" for w in sorted_wr["Win Rate %"]],
                textposition="outside",
                textfont=dict(family="Space Mono", size=10, color="#e8eaf0"),
            ))
            fig_wr.add_hline(y=50, line_dash="dot", line_color="#94a3b8",
                              opacity=0.6, annotation_text="50% breakeven")
            fig_wr.update_layout(
                paper_bgcolor="#0a0e1a", plot_bgcolor="#0d1117",
                font=dict(family="Space Mono", color="#94a3b8", size=11),
                height=320,
                yaxis=dict(gridcolor="#1f2937", range=[0, 110], title="Win Rate %"),
                xaxis=dict(gridcolor="#1f2937"),
                margin=dict(l=10, r=10, t=20, b=10),
                showlegend=False,
            )
            st.plotly_chart(fig_wr, use_container_width=True)

            # ── Total Return bar chart ───────────────────────────
            st.markdown("#### 💰 Total Return per Emiten")
            sorted_ret = valid.sort_values("Total Return %", ascending=False)
            ret_colors = ["#00d4aa" if r >= 0 else "#ff4d6d"
                          for r in sorted_ret["Total Return %"]]
            fig_ret = go.Figure(go.Bar(
                x=sorted_ret["Ticker"],
                y=sorted_ret["Total Return %"],
                marker_color=ret_colors,
                text=[f"{r:+.1f}%" for r in sorted_ret["Total Return %"]],
                textposition="outside",
                textfont=dict(family="Space Mono", size=10, color="#e8eaf0"),
            ))
            fig_ret.add_hline(y=0, line_dash="dot", line_color="#94a3b8", opacity=0.6)
            fig_ret.update_layout(
                paper_bgcolor="#0a0e1a", plot_bgcolor="#0d1117",
                font=dict(family="Space Mono", color="#94a3b8", size=11),
                height=320,
                yaxis=dict(gridcolor="#1f2937", title="Total Return %"),
                xaxis=dict(gridcolor="#1f2937"),
                margin=dict(l=10, r=10, t=20, b=10),
                showlegend=False,
            )
            st.plotly_chart(fig_ret, use_container_width=True)

        # ── Full results table ───────────────────────────────────
        st.markdown("#### 📋 Tabel Lengkap")
        st.caption("Diurutkan berdasarkan Win Rate tertinggi")

        display_df = result_df.copy()
        # Sort valid rows by win rate descending, errors at bottom
        valid_rows  = display_df[display_df["Status"] == "✅"].sort_values("Win Rate %", ascending=False)
        invalid_rows= display_df[display_df["Status"] != "✅"]
        display_df  = pd.concat([valid_rows, invalid_rows]).reset_index(drop=True)

        # Style the table
        def style_row(row):
            styles = [""] * len(row)
            if row["Status"] != "✅":
                return ["color: #4b5563"] * len(row)
            wr_idx = display_df.columns.get_loc("Win Rate %")
            ret_idx = display_df.columns.get_loc("Total Return %")
            try:
                wr = float(row["Win Rate %"])
                styles[wr_idx] = "color: #00d4aa; font-weight: bold" if wr >= 50 else "color: #ff4d6d; font-weight: bold"
            except: pass
            try:
                ret = float(row["Total Return %"])
                styles[ret_idx] = "color: #00d4aa" if ret >= 0 else "color: #ff4d6d"
            except: pass
            return styles

        st.dataframe(
            display_df.style.apply(style_row, axis=1),
            use_container_width=True,
            height=400,
        )

        # Download button
        csv = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name=f"backtest_{ms_strategy.replace('/','-')}_{ms_period}.csv",
            mime="text/csv",
        )

    else:
        st.info("👆 Pilih strategy & konfigurasi di atas, lalu klik **▶ Jalankan Multi-Stock Backtest**")
        st.markdown("""
        **Cara baca tabelnya:**
        - **Win Rate % ≥ 50%** 🟢 → strategy profitable di saham itu
        - **Win Rate % < 50%** 🔴 → strategy kurang cocok
        - **Total Return %** → total keuntungan/kerugian selama periode
        - **Sharpe** → risk-adjusted return (makin tinggi makin bagus, > 1 bagus)
        - **Best/Worst Trade** → trade terbaik & terburuk dalam %
        """)


# ─── FOOTER ─────────────────────────────────────────────────────────
st.markdown("---")
st.caption("⚠️ This platform is for personal educational use only. Not financial advice. DYOR — Do Your Own Research. 🇮🇩")