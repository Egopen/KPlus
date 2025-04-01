using KPProject.BL;
using KPProject.BL.Logger;
using KPProject.DTO.Request;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace KPProject.UI
{
    [Route("Franchisto/[controller]/[action]")]
    [ApiController]
    public class StatisticsController : ControllerBase
    {
        DocsStatsService docsStatsService;
        LoggerService Logger;
        public StatisticsController(DocsStatsService docsStatsService,LoggerService logger) { 
            this.docsStatsService = docsStatsService;
            Logger = logger;
        }

        [HttpPut]
        public async Task<IActionResult> AddStatisticsToDocs(AddStatsToDocsDTO stats)
        {
            Logger.LogInformation("Вход в апи метод добавления статистики");
            var isSuccess=await docsStatsService.AddStatsToDocsAsync(stats);
            if (isSuccess) {
                return Ok();
            }
            Logger.LogInformation("Ошибка при добавление статистики к документу- смотреть логи");
            return BadRequest();
        }
        [HttpPut]
        public async Task<IActionResult> AddStatistics(AddStatsDTO stats)
        {
            Logger.LogInformation($"Попытка добавить статистику: {stats.StatName}, Count: {stats.Count}");

            if (stats.Count < 0)
            {
                Logger.LogWarning("Ошибка: Неправильный формат данных (Count < 0)");
                return BadRequest("Неправильный формат данных");
            }

            var isSuccess = await docsStatsService.AddStatsAsync(stats);
            if (isSuccess)
            {
                Logger.LogInformation("Статистика успешно добавлена/обновлена.");
                return Ok();
            }

            Logger.LogError("Ошибка при добавлении статистики.");
            return BadRequest("Не удалось добавить статистику.");

        }
    }
}
