export const formatDates = (data) => {
    data.forEach(function(entry, index, array) {
        entry.createdAt = new Date(entry.createdAt);
        array[index] = entry;
    });
    return data;
}

export const sortEntries = (entries) => {
    entries.sort(function(a, b){
        return a.createdAt - b.createdAt;
    });
    entries = entries.reverse();
    return entries;
}
