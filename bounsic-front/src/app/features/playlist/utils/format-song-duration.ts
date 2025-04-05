const formatDuration = (duration: string): string => {
    const [hours, minutes] = duration.split(':').map(Number);
    return `${hours} hora${hours !== 1 ? 's' : ''} ${minutes} minuto${minutes !== 1 ? 's' : ''}`;
}
export { formatDuration };