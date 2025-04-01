using System.ComponentModel.DataAnnotations;

namespace KPProject.DTO.Request
{
    public class AddStatsDTO
    {
        [Required]
        public string StatName {  get; set; }
        [Required]
        public int Count {  get; set; }
    }
}
