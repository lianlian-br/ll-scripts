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
  var startDate = Date.parse("2025-06-20");//one day before the execution day 2025-03-23
  const endDate = Date.parse("2025-06-24");

  const availableBalanceUrls = [];
  const paymentCollectionUrls = [];
  while (startDate < endDate) {
    startDate = addDays(startDate, 1);
    availableBalanceUrls.push(
      `http://ll-accounting-prod.us-east-1.elasticbeanstalk.com/providers/BS2/accounting/bank/reconciliation?bankAccountCategory=B2B_TRADE&bankAccountType=AVAILABLE&date=${startDate.toISOString().slice(0, 10)}`
    )
    paymentCollectionUrls.push(
      `http://ll-accounting-prod.us-east-1.elasticbeanstalk.com/providers/BS2/accounting/bank/reconciliation?bankAccountCategory=B2B_TRADE&bankAccountType=PAYMENT_COLLECTION&date=${startDate.toISOString().slice(0, 10)}`
    )
  }

  console.log(availableBalanceUrls);
  console.log(paymentCollectionUrls);

  for (let index = 0; index < availableBalanceUrls.length; index++) {
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

      const availableBalanceUrl = availableBalanceUrls[index];
      console.log(`Executando available balance provider reconciliation -> `, availableBalanceUrl);
      await axios.post(availableBalanceUrl, {}, config);
      console.log(`Executado available balance provider reconciliation -> `, availableBalanceUrl);

      await sleep(5000)

      const paymentCollectionUrl = paymentCollectionUrls[index];
      console.log(`Salvando payment collection balance provider reconciliation -> `, paymentCollectionUrl);
      await axios.post(paymentCollectionUrl, {}, config);
      console.log(`Salvado payment collection balance provider reconciliation -> `, paymentCollectionUrl);

      await sleep(5000)
    } catch (error) {
      console.error("Erro ao fazer as chamadas:", error);
      return;
    }
  }
}

main();

