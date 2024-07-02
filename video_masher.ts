import ffmpeg from 'fluent-ffmpeg';
import path from 'path';
import fs from 'fs';

function resizeVideo(inputPath: string, outputPath: string, targetWidth: number, targetHeight: number): Promise<void> {
    return new Promise((resolve, reject) => {
        ffmpeg(inputPath)
            .outputOptions([
                `-vf scale=${targetWidth}:${targetHeight}:force_original_aspect_ratio=decrease,pad=${targetWidth}:${targetHeight}:(ow-iw)/2:(oh-ih)/2`,
                `-c:a copy`
            ])
            .on('end', () => {
                console.log('Resizing finished!');
                resolve();
            })
            .on('error', (err: Error) => {
                console.log('Error occurred: ' + err.message);
                reject(err);
            })
            .save(outputPath);
    });
}

function concatenateVideos(videoFiles: string[], outputPath: string): Promise<void> {
    return new Promise((resolve, reject) => {
        const ffmpegCommand = ffmpeg();

        videoFiles.forEach(file => {
            ffmpegCommand.input(file);
        });

        ffmpegCommand
            .on('end', () => {
                console.log('Concatenation finished!');
                resolve();
            })
            .on('error', (err: Error) => {
                console.log('Error occurred: ' + err.message);
                reject(err);
            })
            .mergeToFile(outputPath, './temp');
    });
}

async function mashVideos(videoFiles: string[], targetWidth: number = 1080, targetHeight: number = 1920): Promise<void> {
    try {
        const resizedVideos: string[] = [];

        for (const [index, file] of videoFiles.entries()) {
            const outputFilePath = `resized_${index}.mp4`;
            await resizeVideo(file, outputFilePath, targetWidth, targetHeight);
            resizedVideos.push(outputFilePath);
        }

        await concatenateVideos(resizedVideos, 'output_video.mp4');

        // Clean up temporary resized files
        resizedVideos.forEach(file => fs.unlinkSync(file));

        console.log('Final video created successfully!');
    } catch (err) {
        console.error('Error during processing:', err);
    }
}

const videoFiles = process.argv.slice(2);
if (videoFiles.length > 0) {
    mashVideos(videoFiles);
} else {
    console.log("Please provide video file paths as arguments.");
}
