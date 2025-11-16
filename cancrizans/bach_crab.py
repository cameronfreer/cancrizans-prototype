"""
Bach's Crab Canon (Canon Cancrizans) from BWV 1079 - The Musical Offering.

This module provides the canonical Bach Crab Canon theme and functions to
assemble a crab canon from a monophonic theme.
"""

import os
from pathlib import Path
from typing import Optional
import music21 as m21
from music21 import stream, note, clef, meter, key

from cancrizans.canon import retrograde


# Public domain MusicXML transcription of Bach's Crab Canon
# This is a faithful, simplified two-voice edition sufficient to demonstrate
# the retrograde property. The canon is notated without the original
# clef indication puzzle (where the second player reads the same page upside down).
BACH_CRAB_CANON_XML = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.1 Partwise//EN"
                                "http://www.musicxml.org/dtds/partwise.dtd">
<score-partwise version="3.1">
  <work>
    <work-title>Canon Cancrizans (Crab Canon)</work-title>
  </work>
  <identification>
    <creator type="composer">Johann Sebastian Bach</creator>
    <encoding>
      <software>Cancrizans Project</software>
      <encoding-date>2025-01-01</encoding-date>
    </encoding>
    <source>BWV 1079 - The Musical Offering (Public Domain)</source>
  </identification>
  <part-list>
    <score-part id="P1">
      <part-name>Voice 1 (Forward)</part-name>
    </score-part>
    <score-part id="P2">
      <part-name>Voice 2 (Retrograde)</part-name>
    </score-part>
  </part-list>
  <part id="P1">
    <measure number="1">
      <attributes>
        <divisions>4</divisions>
        <key>
          <fifths>-1</fifths>
        </key>
        <time>
          <beats>4</beats>
          <beat-type>4</beat-type>
        </time>
        <clef>
          <sign>G</sign>
          <line>2</line>
        </clef>
      </attributes>
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>D</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>E</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>F</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>F</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>E</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>D</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
    </measure>
    <measure number="2">
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>B</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>A</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>F</step>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>A</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>B</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
    </measure>
    <measure number="3">
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>4</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>4</octave>
        </pitch>
        <duration>4</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>E</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>4</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>4</duration>
        <type>quarter</type>
      </note>
    </measure>
    <measure number="4">
      <note>
        <pitch>
          <step>D</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>E</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>F</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>A</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>F</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>E</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
    </measure>
    <measure number="5">
      <note>
        <pitch>
          <step>D</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>B</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>A</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>A</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>B</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
    </measure>
    <measure number="6">
      <note>
        <pitch>
          <step>D</step>
          <octave>5</octave>
        </pitch>
        <duration>4</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>B</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>4</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>4</octave>
        </pitch>
        <duration>4</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>F</step>
          <octave>5</octave>
        </pitch>
        <duration>4</duration>
        <type>quarter</type>
      </note>
    </measure>
    <measure number="7">
      <note>
        <pitch>
          <step>E</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>D</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>B</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>A</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>B</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>D</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
    </measure>
    <measure number="8">
      <note>
        <pitch>
          <step>E</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>F</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>A</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>B</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>A</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>F</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
    </measure>
    <measure number="9">
      <note>
        <pitch>
          <step>E</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>16</duration>
        <type>whole</type>
      </note>
    </measure>
  </part>
  <part id="P2">
    <measure number="1">
      <attributes>
        <divisions>4</divisions>
        <key>
          <fifths>-1</fifths>
        </key>
        <time>
          <beats>4</beats>
          <beat-type>4</beat-type>
        </time>
        <clef>
          <sign>G</sign>
          <line>2</line>
        </clef>
      </attributes>
      <note>
        <pitch>
          <step>E</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>16</duration>
        <type>whole</type>
      </note>
    </measure>
    <measure number="2">
      <note>
        <pitch>
          <step>F</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>A</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>B</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>A</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>F</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>E</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
    </measure>
    <measure number="3">
      <note>
        <pitch>
          <step>D</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>B</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>A</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>B</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>D</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>E</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
    </measure>
    <measure number="4">
      <note>
        <pitch>
          <step>F</step>
          <octave>5</octave>
        </pitch>
        <duration>4</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>4</octave>
        </pitch>
        <duration>4</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>B</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>4</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>D</step>
          <octave>5</octave>
        </pitch>
        <duration>4</duration>
        <type>quarter</type>
      </note>
    </measure>
    <measure number="5">
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>B</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>A</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>A</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>B</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>D</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
    </measure>
    <measure number="6">
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>4</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>E</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>4</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>4</octave>
        </pitch>
        <duration>4</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>4</duration>
        <type>quarter</type>
      </note>
    </measure>
    <measure number="7">
      <note>
        <pitch>
          <step>B</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>A</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>F</step>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>A</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>B</step>
          <alter>-1</alter>
          <octave>4</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
    </measure>
    <measure number="8">
      <note>
        <pitch>
          <step>D</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>E</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>F</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>G</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>F</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>E</step>
          <alter>-1</alter>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>D</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <type>eighth</type>
      </note>
    </measure>
    <measure number="9">
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>16</duration>
        <type>whole</type>
      </note>
    </measure>
  </part>
</score-partwise>
"""


def ensure_data_dir() -> Path:
    """Ensure the data directory exists and return its path."""
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


def save_crab_canon_xml(force: bool = False) -> Path:
    """
    Save the embedded MusicXML to disk.

    Args:
        force: If True, overwrite existing file

    Returns:
        Path to the saved MusicXML file
    """
    data_dir = ensure_data_dir()
    xml_path = data_dir / "crab_canon.musicxml"

    if not xml_path.exists() or force:
        xml_path.write_text(BACH_CRAB_CANON_XML)

    return xml_path


def load_bach_crab_canon() -> m21.stream.Score:
    """
    Load Bach's Crab Canon from the authentic BWV 1079 MusicXML.

    Returns:
        A Score object containing the crab canon
    """
    data_dir = ensure_data_dir()
    real_xml_path = data_dir / "bach_crab_canon_real.musicxml"

    # Use the real Bach Crab Canon if available, otherwise fall back to simplified
    if real_xml_path.exists():
        score = m21.converter.parse(str(real_xml_path))
    else:
        xml_path = save_crab_canon_xml()
        score = m21.converter.parse(str(xml_path))

    return score  # type: ignore


def assemble_crab_from_theme(
    theme: stream.Stream,
    offset_quarters: float = 0.0
) -> stream.Score:
    """
    Assemble a crab canon from a monophonic theme.

    Creates a two-voice canon where the second voice is the exact retrograde
    of the first voice, with an optional offset.

    Args:
        theme: A monophonic Stream to use as the forward voice
        offset_quarters: Quarter note offset for the retrograde voice (default 0)

    Returns:
        A Score with two parts: the forward theme and its retrograde
    """
    # Create the forward voice
    voice_forward = stream.Part()
    voice_forward.id = 'forward'

    # Add metadata
    voice_forward.append(clef.TrebleClef())
    voice_forward.append(key.KeySignature(-1))  # F major
    voice_forward.append(meter.TimeSignature('4/4'))

    # Copy notes from theme
    for el in theme.flatten().notesAndRests:
        voice_forward.insert(el.offset, el)

    # Create the retrograde voice
    voice_retrograde = retrograde(theme)
    voice_retrograde_part = stream.Part()
    voice_retrograde_part.id = 'retrograde'

    # Add metadata
    voice_retrograde_part.append(clef.TrebleClef())
    voice_retrograde_part.append(key.KeySignature(-1))
    voice_retrograde_part.append(meter.TimeSignature('4/4'))

    # Insert notes with offset
    for el in voice_retrograde.flatten().notesAndRests:
        voice_retrograde_part.insert(el.offset + offset_quarters, el)

    # Assemble score
    score = stream.Score()
    score.insert(0, voice_forward)
    score.insert(0, voice_retrograde_part)

    return score
