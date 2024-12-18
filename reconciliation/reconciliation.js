const axios = require("axios");

function addDays(date, days) {
  var result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
  var startDate = Date.parse("2024-12-10");//one day before the execution day
  const endDate = Date.parse("2024-12-13");
  const merchantId = 152;

  const accountingUrls = [];
  const balanceUrls = [];
  while (startDate < endDate) {
    startDate = addDays(startDate, 1);
    accountingUrls.push(
      `http://ll-transaction.us-east-1.elasticbeanstalk.com/merchant-reconciliation/?paymentMethod=PIX,BOLETO,CREDIT_CARD&endDateTime=${startDate
        .toISOString()
        .slice(
          0,
          10
        )} 23:59:59.999999&merchantsToRunReconciliation=${merchantId}`
    );
    balanceUrls.push(
      `http://ll-transaction.us-east-1.elasticbeanstalk.com/merchant-reconciliation/save-balance?date=${startDate
        .toISOString()
        .slice(0, 10)}&merchantsToRunReconciliation=${merchantId}`
    );
  }

  console.log(accountingUrls);
  console.log(balanceUrls);

  for (let index = 0; index < accountingUrls.length; index++) {
    try {
      const response = await axios.post(
        "http://auth.llpaybr.local/ll/application/generate/jwt",
        "grant_type=client_credentials&application=prod",
        {
          proxy: {
            protocol: "http",
            host: "127.0.0.1",
            port: 8080,
          },
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      const config = {
        proxy: {
          protocol: "http",
          host: "127.0.0.1",
          port: 8080,
        },
        headers: { Authorization: `Bearer ${response.data.token}` },
      };

      const accountingUrl = accountingUrls[index];
      console.log(`Executando accounting -> `, accountingUrl);
      await axios.post(accountingUrl, {}, config);
      console.log(`Executado accounting -> `, accountingUrl);

      await sleep(20000)

      const balanceUrl = balanceUrls[index];
      console.log(`Salvando balance -> `, balanceUrl);
      await axios.post(balanceUrl, {}, config);
      console.log(`Salvado balance -> `, balanceUrl);

      await sleep(5000)
    } catch (error) {
      console.error("Erro ao fazer as chamadas:", error);
      return;
    }
  }
}

main();

