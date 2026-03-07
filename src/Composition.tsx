import React from 'react';
import {Series, AbsoluteFill, OffthreadVideo, Html5Audio, Img, CalculateMetadataFunction, staticFile} from 'remotion';
import {parseMedia} from '@remotion/media-parser';


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


export const Video: React.FC<MediaSrcProp> = ({src}) => {
  return (
      <AbsoluteFill>
        <OffthreadVideo src={src} />
      </AbsoluteFill>
  );
};

export const Logo: React.FC<MediaSrcProp> = ({src}) => {
  return (
    <AbsoluteFill>
        <Img 
           src={src}
            style={{
              transform: 'scale(0.40) translateY(-340px)',
            }}/>
     </AbsoluteFill>
  );
};

export const Audio: React.FC<MediaSrcProp> = ({src}) => {
  return (
    <AbsoluteFill>
      <Html5Audio src={src} />
    </AbsoluteFill>
  );
};


type VideoToEmbed = {
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
            <OffthreadVideo volume={0} src={vid.src} />
          </Series.Sequence>
        );
      })}
    </Series>
  );
};


export const calculateMetadata: CalculateMetadataFunction<MyCompProp> = async ({props}) => {
  const fps = 30;
  const videos = await Promise.all([
    ...props.videosSrc.map(async (video): Promise<VideoToEmbed> => {
      const {slowDurationInSeconds} = await parseMedia({
        src: video.src,
        fields: {
          slowDurationInSeconds: true,
        },
      });

      return {
        durationInFrames: Math.min(Math.floor(slowDurationInSeconds * fps), Math.floor(7 * fps)),
        src: video.src,
      };
    }),
  ]);

  // const totalDurationInFrames = videos.reduce((acc, video) => acc + (video.durationInFrames ?? 0), 0);
  const {slowDurationInSeconds} = await parseMedia({
    src: props.audioSrc,
    fields: {
      slowDurationInSeconds: true,
      // dimensions: true,
    },
  });
  return {
    props: {
      ...props,
      videosSrc: videos,
    },
    fps,
    durationInFrames: Math.floor(slowDurationInSeconds * fps),
  };
};


