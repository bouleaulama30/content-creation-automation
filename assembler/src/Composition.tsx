import React from 'react';
import {Series, AbsoluteFill, OffthreadVideo, Html5Audio, Img, CalculateMetadataFunction, staticFile} from 'remotion';


type MediaSrcProp = {
  src: string;
};

type MyCompProp = {
  videosSrc: VideoToEmbed[];
  audioSrc: string;
  logoSrc: string;
}

export const MyComp: React.FC<MyCompProp> = ({videosSrc, audioSrc, logoSrc}) => {
  return (
    <AbsoluteFill>
      <VideosInSequence videos={videosSrc}/>
      <Audio src={audioSrc} />
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
              transform: 'scale(0.40) translateY(-340px)',
            }}/>
     </AbsoluteFill>
  );
};

export const Audio: React.FC<MediaSrcProp> = ({src}) => {
  return (
    <AbsoluteFill>
      <Html5Audio src={staticFile(src)} />
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
            <OffthreadVideo volume={0} src={staticFile(vid.src)} />
          </Series.Sequence>
        );
      })}
    </Series>
  );
};


export const calculateMetadata: CalculateMetadataFunction<MyCompProp> = async ({props}) => {
  const fps = 30;

  // On additionne simplement les durées que Python a mises dans le JSON
  const totalDurationInFrames = props.videosSrc.reduce(
    (acc, video) => acc + (video.durationInFrames ?? 0), 
    0
  );

  return {
    props, // On transmet les données reçues sans les modifier
    fps,
    durationInFrames: totalDurationInFrames,
  };
};


