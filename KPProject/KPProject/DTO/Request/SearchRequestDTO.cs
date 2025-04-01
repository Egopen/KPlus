using System.ComponentModel.DataAnnotations;

namespace KPProject.DTO.Request
{
    public class SearchRequestDTO
    {
        [Required]
        public string Query {  get; set; }
        [Required]
        public int Page { get; set; }
    }
}
