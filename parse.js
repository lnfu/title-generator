function parse() {
    const getElementByXpath = (path) => document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    const channelXpath  = '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[1]/ytd-video-owner-renderer/div[1]/ytd-channel-name/div/div/yt-formatted-string/a'
    const titleXpath    = '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[1]/h1/yt-formatted-string'
    const durationSelector = '#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > div.ytp-time-display.notranslate > span:nth-child(2) > span.ytp-time-duration'

    const channel  = getElementByXpath(channelXpath).innerText;
    const title    = getElementByXpath(titleXpath).innerText;
    const duration = document.querySelector(durationSelector).innerText;
    const videoID  = window.location.search.match(/^\?v=(.*)$/)[1];
    const csvLine = `"${channel}","${title}","${duration}","${videoID}"`;
    console.log(csvLine);
    navigator.clipboard.writeText(csvLine);
};
setTimeout(parse, 2000);
// You should focus back before timeout.