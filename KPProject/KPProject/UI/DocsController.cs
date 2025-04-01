using System.ComponentModel.DataAnnotations;
using Elastic.Clients.Elasticsearch;
using KPProject.BL;
using KPProject.BL.Logger;
using KPProject.DAL.documents_db;
using KPProject.DTO.Request;
using KPProject.DTO.ServicesToUI;
using Microsoft.AspNetCore.Cors.Infrastructure;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace KPProject.UI
{
    [Route("Franchisto/[controller]/[action]")]
    [ApiController]
    public class DocsController : ControllerBase
    {
        LoggerService logger;
        DocsService docsService;
        public DocsController( DocsService docsService,LoggerService logger) { 
            this.docsService = docsService;
            this.logger = logger;
        }

        [HttpGet]
        public async Task<IActionResult> SearchByQuery([FromQuery,Required] string query, [FromQuery] int page=1)
        {
            logger.LogInformation("Произошел вход в метод SearchByQuery");
            if (string.IsNullOrEmpty(query))
            {
                logger.LogInformation("Произошел выход из-за неправильного ввода строки в метод SearchByQuery");
                return BadRequest("Query is required.");
            }
            if (page < 1)
            {
                logger.LogInformation("Произошел выход из-за неправильного ввода страницы в метод SearchByQuery");
                return BadRequest("Wrong page");
            }
            IEnumerable<ElasticDocsDTO> docs;
            try
            {
                docs = await docsService.SearchDocsAsync(query, page);
            }
            catch (Exception ex) {
                logger.LogError($"Произошла ошибка {ex.Message} в методе SearchByQuery");
                return BadRequest("Something went wrong");
            }
            logger.LogInformation("Произошел выход в метод SearchByQuery");
            return Ok(docs);
        }
        [HttpGet]
        public async Task<IActionResult> GetStartDocs([FromQuery] int page = 1)
        {
            logger.LogInformation("Произошел вход в метод GetStartDocs");
            if (page < 1)
            {
                logger.LogInformation("Произошел выход из-за неправильного ввода страницы в метод GetStartDocs");
                return BadRequest("Wrong page");
            }
            IEnumerable<BriefDocsDTO> docs;
            try
            {
                docs = await docsService.GetPopularDocs(page);
            }
            catch (Exception ex) {
                logger.LogError($"Произошла ошибка {ex.Message} в методе GetStartDocs");
                return BadRequest("Something went wrong");
            }
            logger.LogInformation("Произошел выход в метод GetStartDocs");
            return Ok(docs);
        }
        [HttpGet]
        public async Task<IActionResult> GetDocById([FromQuery,Required] int id)
        {
            logger.LogInformation("Произошел вход в метод GetStartDocs");
            if (id < 1)
            {
                logger.LogInformation($"Неправильный формат id на вход GetStartDocs id {id}, выход из метоад");
                return BadRequest("Неправильный формат данных на вход");
            }
            try
            {
                var doc = await docsService.GetDocAsync(id);
                logger.LogInformation("Поиск успешен, выход из метода GetStartDocs");
                return Ok(doc);

            }
            catch (Exception ex)
            {
                logger.LogError($"Ошибка в апи методе GetStaartDocs: {ex.Message}, выход из метода GetStartDocs");
                return BadRequest("Ошибка при получении данных");
            }
        }


    }
}
