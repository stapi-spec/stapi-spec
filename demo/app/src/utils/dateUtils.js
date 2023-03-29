function formatToISOString(range){
  return `${range[0].toISOString()}/${range[1].toISOString()}`;
}

function formatToFriendlyString(date) {
  const shorterDate = date.split('.')[0]
  return shorterDate.substring().replace('T', ' ');
}

function parseStacDatetime(datetime) {
  const splitDates = datetime.split('/');
  if (splitDates.length > 1) {
    return {
      start: splitDates[0],
      end: splitDates[1]
    }
  }

  return {
    start: datetime,
    end: datetime,
  }
}

export {
  formatToISOString,
  formatToFriendlyString,
  parseStacDatetime
};
