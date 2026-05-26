// speedtest.js — скрипт для HTTP Request Shortcuts
// Размещается на GitHub и выполняется приложением

// Функция рандомизации скорости
function generateSpeed(tariffSpeed) {
    var multiplier = 0.90 + Math.random() * 0.15; // 0.90-1.05
    var download = Math.round(tariffSpeed * multiplier * 100) / 100;
    var upload = Math.round(download * (0.75 + Math.random() * 0.15) * 100) / 100;
    return { download: download, upload: upload };
}

// Функция рандомизации пинга
function generatePing(downloadSpeed) {
    var basePing;
    if (downloadSpeed >= 400) basePing = Math.floor(Math.random() * 3) + 1;
    else if (downloadSpeed >= 200) basePing = Math.floor(Math.random() * 4) + 2;
    else if (downloadSpeed >= 100) basePing = Math.floor(Math.random() * 5) + 4;
    else basePing = Math.floor(Math.random() * 8) + 8;
    
    return {
        ping: basePing,
        jitter: Math.floor(Math.random() * 5) + 1,
        ping_download: basePing + Math.floor(Math.random() * 4),
        ping_upload: basePing + Math.floor(Math.random() * 5) + 1
    };
}

// ГЛАВНАЯ ФУНКЦИЯ — выполняется в HTTP Request Shortcuts
function execute(input) {
    // input содержит переменные: account, tariff
    var speeds = generateSpeed(parseInt(input.tariff));
    var pings = generatePing(speeds.download);
    
    // Формируем payload
    var payload = {
        download: speeds.download,
        upload: speeds.upload,
        ping: pings.ping,
        jitter: pings.jitter,
        ping_download: pings.ping_download,
        ping_upload: pings.ping_upload,
        finger_hash: "5bcf1c243042e72317f2b58a919bd299",
        server_id: 47,
        city: "Улан-Удэ",
        requester: "user",
        lat: 51.8334492,
        lng: 107.584068,
        region_id: 24,
        exam_type: 1,
        vpn_flag: 0,
        ya_user: "1775491083143397116",
        rtk_nls: input.account,
        attr_2: "cookie_accept",
        attr_3: "multi",
        attr_4: "2.7.2",
        country: "Россия",
        timezone: "Asia/Irkutsk",
        network_type: "wi-fi",
        device_type: "n/a",
        trait: "service"
    };
    
    // Возвращаем результат для отправки
    return {
        url: "https://www.qms.ru/api/exam_result",
        method: "POST",
        headers: {
            "x-api-key": "b8a4ecb62a2cc6bb375e01c9482c996d",
            "origin": "https://epd.qms.ru",
            "referer": "https://epd.qms.ru/"
        },
        body: payload,
        bodyType: "form"
    };
}
