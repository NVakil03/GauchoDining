async function loadMealsLastTwoWeeks() {
    const diningCommons = ['de-la-guerra'];
    const today = new Date();
    const headers = {
        "accept": "application/json",
        "ucsb-api-key": "msK15c7pUiSOGRQXmpW7w4zW6GrldYht"
    };

    console.log("Name,Station\n");

    for (let i = 26; i >= 12; i--) {
        const tempDate = new Date(today);
        tempDate.setDate(today.getDate() - (today.getDate() - i));
        const dateStr = tempDate.toISOString().split('T')[0];

        const dayOfWeek = tempDate.getDay();
        const meals = (dayOfWeek === 5 || dayOfWeek === 6)
            ? ['brunch', 'dinner']
            : ['breakfast', 'lunch', 'dinner'];

        for (const diningCommon of diningCommons) {
            for (const meal of meals) {
                const url = `https://api.ucsb.edu/dining/menu/v1/${dateStr}/${diningCommon}/${meal}`;

                try {
                    const response = await fetch(url, { headers });
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    const data = await response.json();

                    const items = data.map(item => ({
                        name: item.name,
                        station: item.station
                    }));

                    items.forEach(item => {
                        console.log(`${item.name}`);
                    });
                } catch (error) {
                    console.error(`❌ Failed to load ${dateStr} ${diningCommon} ${meal}`, error);
                }
            }
        }
    }
}


loadMealsLastTwoWeeks();
