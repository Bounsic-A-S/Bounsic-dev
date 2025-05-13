export function formatDuration(duration: number): string {
    if (typeof duration !== 'number' || isNaN(duration)) return '00:00';
  
    const minutes = Math.floor(duration / 60);
    const seconds = Math.floor(duration % 60);
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  }
  