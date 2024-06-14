const axios = require("axios");

function addDays(date, days) {
  var result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
}

async function main() {
  var startDate = Date.parse("2023-05-14");
  const endDate = Date.parse("2024-06-12");

  const accountingUrls = [];
  const balanceUrls = [];
  while (startDate < endDate) {
    startDate = addDays(startDate, 1);
    accountingUrls.push(
      `http://ll-transaction.us-east-1.elasticbeanstalk.com/merchant-reconciliation/?paymentMethod=PIX,BOLETO,CREDIT_CARD&endDateTime=${startDate
        .toISOString()
        .slice(0, 10)} 23:59:59.999999&merchantsToRunReconciliation=103`
    );
    balanceUrls.push(
      `http://ll-transaction.us-east-1.elasticbeanstalk.com/merchant-reconciliation/save-balance?date=${startDate
        .toISOString()
        .slice(0, 10)}&merchantsToRunReconciliation=103`
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
      await axios.post(accountingUrl, {}, config);
      console.log(`Executando accounting -> `, accountingUrl);

      const balanceUrl = balanceUrls[index];
      await axios.post(balanceUrl, {}, config);
      console.log(`Salvando balance -> `, balanceUrl);
    } catch (error) {
      console.error("Erro ao fazer as chamadas:", error);
      return;
    }
  }
}

main();
