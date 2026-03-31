import React from 'react';
import {Series, AbsoluteFill, OffthreadVideo, Html5Audio, Img, CalculateMetadataFunction, staticFile, } from 'remotion';
import {parseMedia} from '@remotion/media-parser';

type MediaSrcProp = {
  src: string;
};

type AudioSrcProp = {
  src: string;
  volume: number;
};

type MyCompProp = {
  videosSrc: VideoToEmbed[];
  audioSrc1: string;
  audioSrc2Prop: AudioSrcProp;
  logoSrc: string;
}

export const MyComp: React.FC<MyCompProp> = ({videosSrc, audioSrc1, audioSrc2Prop, logoSrc}) => {
  const volume: number = audioSrc2Prop.volume;
  return (
    <AbsoluteFill>
      <VideosInSequence videos={videosSrc}/>
      {/* 2. Filtre de couleur "Sagesse / Cinématique" (Teinte chaude et profonde) */}
      {/* <AbsoluteFill 
        style={{
          backgroundColor: '#3b240e', // Un marron chaud / doré sombre (Ambiance Kung Fu Panda)
          mixBlendMode: 'soft-light', // Fusion douce avec la vidéo
          opacity: 0.4, // Assez présent pour lier toutes les vidéos ensemble
        }} 
      /> */}

      {/* 3. Dégradé sombre pour faire ressortir les sous-titres et centrer l'attention */}
      <AbsoluteFill 
        style={{
          // Dégradé : transparent en haut, noir à 80% en bas
          background: 'linear-gradient(to bottom, rgba(0,0,0,0) 50%, rgba(0,0,0,0.6) 100%)',
          pointerEvents: 'none',
        }} 
      />
      <Audio src={audioSrc1} volume={1} />
      <Audio src={audioSrc2Prop.src} volume={volume}/>
      <Logo src={logoSrc} />
    </AbsoluteFill>
  );
};

export const Logo: React.FC<MediaSrcProp> = ({src}) => {
  return (
    <AbsoluteFill>
        <Img 
           src={staticFile(src)}
            style={{
              transform: 'scale(0.40) translateY(2930px)',
            }}/>
     </AbsoluteFill>
  );
};

export const Audio: React.FC<AudioSrcProp> = ({src, volume}) => {
  return (
    <AbsoluteFill>
      <Html5Audio src={staticFile(src)} volume={volume} />
    </AbsoluteFill>
  );
};


export type VideoToEmbed = {
  src: string;
  durationInFrames: number | null;
};

type Props = {
  videos: VideoToEmbed[];
};

export const VideosInSequence: React.FC<Props> = ({videos}) => {
  return (
    <Series>
      {videos.map((vid) => {
        if (vid.durationInFrames === null) {
          throw new Error('Could not get video duration');
        }

        return (
          <Series.Sequence key={vid.src} durationInFrames={vid.durationInFrames}>
            <OffthreadVideo volume={0} src={staticFile(vid.src)}  style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                // On baisse la saturation de 15% et on augmente le contraste pour un look "dramatique"
                // filter: 'saturate(0.85) contrast(1.15)',
              }}/>
          </Series.Sequence>
        );
      })}
    </Series>
  );
};


export const calculateMetadata: CalculateMetadataFunction<MyCompProp> = async ({props}) => {
  const fps = 30;

  const {slowDurationInSeconds} = await parseMedia({
    src: staticFile(props.audioSrc1), 
    fields: {
      slowDurationInSeconds: true,
    },
  });

  return {
    props, // On transmet les données reçues sans les modifier
    fps,
    durationInFrames: Math.floor(slowDurationInSeconds * fps),  };
};

