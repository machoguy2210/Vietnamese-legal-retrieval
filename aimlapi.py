from openai import OpenAI

client = OpenAI(
    api_key="6f32573452e3473799da5b29f021ffb6",
    base_url="https://api.aimlapi.com",
)

response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
    messages=[
        {
            "role": "system",
            "content": '''You are an advanced legal query generator with specialized skills in analyzing legal documents. When provided with an excerpt from a legal document, your task is to identify 1 - 5 critical aspects or implications that might interest or impact the readers. These aspects should address various dimensions of the content, focusing on rights, obligations, potential legal issues, or general legal awareness, exclusively within provided grounded content. Do not consider information in document's source for this analysis. 
            For each identified critical aspect, generate a single question. These questions should reflect plausible inquiries that an average citizen might have, relating directly to the document but formulated in a manner accessible to someone unfamiliar with the presence of the legal text or information being asked about. Phrase the questions as if coming from a layperson who has not read or seen the legal text ever.
            Your output should be in JSON format, listing the critical aspects identified and a corresponding question for each aspect. Please adhere to the following guidelines for creating questions:
            -    Think creatively about real-world scenarios and edge cases the law might apply to, phrase it naturally as if asked by an average citizen.
            -    The queries should be ones that could reasonably be answered by the information exclusively within provided grounded content only. Do not ask information in document's source.
            -    Each query should be one sentence only and its length is no more than 120 words.
            -    Try to phrase each of the questions as detailed as possible, as if you haven't never seen the legal text and are trying to look for it using keywords in the question, you may need to include details in document's source and domain for this aim. You should not quote the exact legal text code (like 02/2017/TT-BQP). The better way is to include information on the content of document as in document's source instead like the executive body published the document (e.g. "Bộ Y tế quy định thế nào về ..."). In the case you have to refer to the legal text, use words like: "Quy định pháp luật", "Pháp luật", "Luật". Don't use the word "này".
            -    Present your analysis and questions in Vietnamese. 
            ...
            Structure your output in the JSON format below:
            ```
            {
            "aspects": [
                [Brief description of the aspect 1],
                [Brief description of the aspect 2],
                ...
            ],
            "questions": [
                [Your question related to aspect 1 of the legal text],
                [Your question related to aspect 2 of the legal text],
                ...
            ]
            }
            ```
            Ensure to replace the placeholders with actual analysis and questions based on the legal text provided, and in Vietnamese. Answer with the JSON and nothing else.
            ''',
        },
        {
            "role": "user",
            "content": '''
            The following is the mentioned excerpt:
            
Chương I.

CHẾ ĐỘ CHÍNH TRỊ

Điều 1.

Nước Cộng hòa xã hội chủ nghĩa Việt Nam là một nước độc lập, có chủ quyền, thống nhất và toàn vẹn lãnh thổ, bao gồm đất liền, hải đảo, vùng biển và vùng trời.

Điều 2.

1. Nhà nước Cộng hòa xã hội chủ nghĩa Việt Nam là nhà nước pháp quyền xã hội chủ nghĩa của Nhân dân, do Nhân dân, vì Nhân dân.

2. Nước Cộng hòa xã hội chủ nghĩa Việt Nam do Nhân dân làm chủ; tất cả quyền lực nhà nước thuộc về Nhân dân mà nền tảng là liên minh giữa giai cấp công nhân với giai cấp nông dân và đội ngũ trí thức.

3. Quyền lực nhà nước là thống nhất, có sự phân công, phối hợp, kiểm soát giữa các cơ quan nhà nước trong việc thực hiện các quyền lập pháp, hành pháp, tư pháp.

Điều 3.

Nhà nước bảo đảm và phát huy quyền làm chủ của Nhân dân; công nhận, tôn trọng, bảo vệ và bảo đảm quyền con người, quyền công dân; thực hiện mục tiêu dân giàu, nước mạnh, dân chủ, công bằng, văn minh, mọi người có cuộc sống ấm no, tự do, hạnh phúc, có điều kiện phát triển toàn diện.

Điều 4.

1. Đảng Cộng sản Việt Nam - Đội tiên phong của giai cấp công nhân, đồng thời là đội tiên phong của Nhân dân lao động và của dân tộc Việt Nam, đại biểu trung thành lợi ích của giai cấp công nhân, nhân dân lao động và của cả dân tộc, lấy chủ nghĩa Mác - Lênin và tư tưởng Hồ Chí Minh làm nền tảng tư tưởng, là lực lượng lãnh đạo Nhà nước và xã hội.

2. Đảng Cộng sản Việt Nam gắn bó mật thiết với Nhân dân, phục vụ Nhân dân, chịu sự giám sát của Nhân dân, chịu trách nhiệm trước Nhân dân về những quyết định của mình.

3. Các tổ chức của Đảng và đảng viên Đảng Cộng sản Việt Nam hoạt động trong khuôn khổ Hiến pháp và pháp luật.

Điều 5.

1. Nước Cộng hòa xã hội chủ nghĩa Việt Nam là quốc gia thống nhất của các dân tộc cùng sinh sống trên đất nước Việt Nam.

2. Các dân tộc bình đẳng, đoàn kết, tôn trọng và giúp nhau cùng phát triển; nghiêm cấm mọi hành vi kỳ thị, chia rẽ dân tộc.

3. Ngôn ngữ quốc gia là tiếng Việt. Các dân tộc có quyền dùng tiếng nói, chữ viết, giữ gìn bản sắc dân tộc, phát huy phong tục, tập quán, truyền thống và văn hóa tốt đẹp của mình.

4. Nhà nước thực hiện chính sách phát triển toàn diện và tạo điều kiện để các dân tộc thiểu số phát huy nội lực, cùng phát triển với đất nước.

Điều 6.

Nhân dân thực hiện quyền lực nhà nước bằng dân chủ trực tiếp, bằng dân chủ đại diện thông qua Quốc hội, Hội đồng nhân dân và thông qua các cơ quan khác của Nhà nước.

Điều 7.

1. Việc bầu cử đại biểu Quốc hội và đại biểu Hội đồng nhân dân được tiến hành theo nguyên tắc phổ thông, bình đẳng, trực tiếp và bỏ phiếu kín.

2. Đại biểu Quốc hội, đại biểu Hội đồng nhân dân bị cử tri hoặc Quốc hội, Hội đồng nhân dân bãi nhiệm khi không còn xứng đáng với sự tín nhiệm của Nhân dân.

Điều 8.

1. Nhà nước được tổ chức và hoạt động theo Hiến pháp và pháp luật, quản lý xã hội bằng Hiến pháp và pháp luật, thực hiện nguyên tắc tập trung dân chủ.

2. Các cơ quan nhà nước, cán bộ, công chức, viên chức phải tôn trọng Nhân dân, tận tụy phục vụ Nhân dân, liên hệ chặt chẽ với Nhân dân, lắng nghe ý kiến và chịu sự giám sát của Nhân dân; kiên quyết đấu tranh chống tham nhũng, lãng phí và mọi biểu hiện quan liêu, hách dịch, cửa quyền.

Điều 9.

1. Mặt trận Tổ quốc Việt Nam là tổ chức liên minh chính trị, liên hiệp tự nguyện của tổ chức chính trị, các tổ chức chính trị - xã hội, tổ chức xã hội và các cá nhân tiêu biểu trong các giai cấp, tầng lớp xã hội, dân tộc, tôn giáo, người Việt Nam định cư ở nước ngoài.

Mặt trận Tổ quốc Việt Nam là cơ sở chính trị của chính quyền nhân dân; đại diện, bảo vệ quyền và lợi ích hợp pháp, chính đáng của Nhân dân; tập hợp, phát huy sức mạnh đại đoàn kết toàn dân tộc, thực hiện dân chủ, tăng cường đồng thuận xã hội; giám sát, phản biện xã hội; tham gia xây dựng Đảng, Nhà nước, hoạt động đối ngoại nhân dân góp phần xây dựng và bảo vệ Tổ quốc.

2. Công đoàn Việt Nam, Hội nông dân Việt Nam, Đoàn thanh niên cộng sản Hồ Chí Minh, Hội liên hiệp phụ nữ Việt Nam, Hội cựu chiến binh Việt Nam là các tổ chức chính trị - xã hội được thành lập trên cơ sở tự nguyện, đại diện và bảo vệ quyền, lợi ích hợp pháp, chính đáng của thành viên, hội viên tổ chức mình; cùng các tổ chức thành viên khác của Mặt trận phối hợp và thống nhất hành động trong Mặt trận Tổ quốc Việt Nam.

3. Mặt trận Tổ quốc Việt Nam, các tổ chức thành viên của Mặt trận và các tổ chức xã hội khác hoạt động trong khuôn khổ Hiến pháp và pháp luật. Nhà nước tạo điều kiện để Mặt trận Tổ quốc Việt Nam các tổ chức thành viên của Mặt trận và các tổ chức xã hội khác hoạt động.

Điều 10.

Công đoàn Việt Nam là tổ chức chính trị - xã hội của giai cấp công nhân và của người lao động được thành lập trên cơ sở tự nguyện, đại diện cho người lao động, chăm lo và bảo vệ quyền, lợi ích hợp pháp, chính đáng của người lao động; tham gia quản lý nhà nước, quản lý kinh tế - xã hội; tham gia kiểm tra, thanh tra, giám sát hoạt động của cơ quan nhà nước, tổ chức, đơn vị, doanh nghiệp về những vấn đề liên quan đến quyền, nghĩa vụ của người lao động; tuyên truyền, vận động người lao động học tập, nâng cao trình độ, kỹ năng nghề nghiệp, chấp hành pháp luật, xây dựng và bảo vệ Tổ quốc.

Điều 11.

1. Tổ quốc Việt Nam là thiêng liêng, bất khả xâm phạm.

2. Mọi hành vi chống lại độc lập, chủ quyền, thống nhất và toàn vẹn lãnh thổ, chống lại sự nghiệp xây dựng và bảo vệ Tổ quốc đều bị nghiêm trị.

Điều 12.

Nước Cộng hòa xã hội chủ nghĩa Việt Nam thực hiện nhất quán đường lối đối ngoại độc lập, tự chủ, hòa bình, hữu nghị, hợp tác và phát triển; đa phương hóa, đa dạng hóa quan hệ, chủ động và tích cực hội nhập, hợp tác quốc tế trên cơ sở tôn trọng độc lập, chủ quyền và toàn vẹn lãnh thổ, không can thiệp vào công việc nội bộ của nhau, bình đẳng, cùng có lợi; tuân thủ Hiến chương Liên hợp quốc và điều ước quốc tế mà Cộng hòa xã hội chủ nghĩa Việt Nam là thành viên; là bạn, đối tác tin cậy và thành viên có trách nhiệm trong cộng đồng quốc tế vì lợi ích quốc gia, dân tộc, góp phần vào sự nghiệp hòa bình, độc lập dân tộc, dân chủ và tiến bộ xã hội trên thế giới.

Điều 13.

1. Quốc kỳ nước Cộng hòa xã hội chủ nghĩa Việt Nam hình chữ nhật, chiều rộng bằng hai phần ba chiều dài, nền đỏ, ở giữa có ngôi sao vàng năm cánh.

2. Quốc huy nước Cộng hòa xã hội chủ nghĩa Việt Nam hình tròn, nền đỏ, ở giữa có ngôi sao vàng năm cánh, xung quanh có bông lúa, ở dưới có nửa bánh xe răng và dòng chữ Cộng hòa xã hội chủ nghĩa Việt Nam.

3. Quốc ca nước Cộng hòa xã hội chủ nghĩa Việt Nam là nhạc và lời của bài Tiến quân ca.

4. Quốc khánh nước Cộng hòa xã hội chủ nghĩa Việt Nam là ngày Tuyên ngôn độc lập 2 tháng 9 năm 1945.

5. Thủ đô nước Cộng hòa xã hội chủ nghĩa Việt Nam là Hà Nội.

Chương II.

QUYỀN CON NGƯỜI, QUYỀN VÀ NGHĨA VỤ CƠ BẢN CỦA CÔNG DÂN

Điều 14.

1. Ở nước Cộng hòa xã hội chủ nghĩa Việt Nam, các quyền con người, quyền công dân về chính trị, dân sự, kinh tế, văn hóa, xã hội được công nhận, tôn trọng, bảo vệ, bảo đảm theo Hiến pháp và pháp luật.

2. Quyền con người, quyền công dân chỉ có thể bị hạn chế theo quy định của luật trong trường hợp cần thiết vì lý do quốc phòng, an ninh quốc gia, trật tự, an toàn xã hội, đạo đức xã hội, sức khỏe của cộng đồng.

Điều 15.

1. Quyền công dân không tách rời nghĩa vụ công dân.

2. Mọi người có nghĩa vụ tôn trọng quyền của người khác.

3. Công dân có trách nhiệm thực hiện nghĩa vụ đối với Nhà nước và xã hội.

4. Việc thực hiện quyền con người, quyền công dân không được xâm phạm lợi ích quốc gia, dân tộc, quyền và lợi ích hợp pháp của người khác.

Điều 16.

1. Mọi người đều bình đẳng trước pháp luật.

2. Không ai bị phân biệt đối xử trong đời sống chính trị, dân sự, kinh tế, văn hóa, xã hội.

Điều 17.

1. Công dân nước Cộng hòa xã hội chủ nghĩa Việt Nam là người có quốc tịch Việt Nam.

2. Công dân Việt Nam không thể bị trục xuất, giao nộp cho nhà nước khác.

3. Công dân Việt Nam ở nước ngoài được Nhà nước Cộng hòa xã hội chủ nghĩa Việt Nam bảo hộ.

Điều 18.

1. Người Việt Nam định cư ở nước ngoài là bộ phận không tách rời của cộng đồng dân tộc Việt Nam.

2. Nhà nước Cộng hòa xã hội chủ nghĩa Việt Nam khuyến khích và tạo điều kiện để người Việt Nam định cư ở nước ngoài giữ gìn và phát huy bản sắc văn hóa dân tộc Việt Nam, giữ quan hệ gắn bó với gia đình và quê hương, góp phần xây dựng quê hương, đất nước.

Điều 19.

Mọi người có quyền sống. Tính mạng con người được pháp luật bảo hộ. Không ai bị tước đoạt tính mạng trái luật.

Điều 20.

1. Mọi người có quyền bất khả xâm phạm về thân thể, được pháp luật bảo hộ về sức khoẻ, danh dự và nhân phẩm; không bị tra tấn, bạo lực, truy bức, nhục hình hay bất kỳ hình thức đối xử nào khác xâm phạm thân thể, sức khỏe, xúc phạm danh dự, nhân phẩm.

2. Không ai bị bắt nếu không có quyết định của Tòa án nhân dân, quyết định hoặc phê chuẩn của Viện kiểm sát nhân dân, trừ trường hợp phạm tội quả tang. Việc bắt, giam, giữ người do luật định.

3. Mọi người có quyền hiến mô, bộ phận cơ thể người và hiến xác theo quy định của luật. Việc thử nghiệm y học, dược học, khoa học hay bất kỳ hình thức thử nghiệm nào khác trên cơ thể người phải có sự đồng ý của người được thử nghiệm.

Điều 21.

1. Mọi người có quyền bất khả xâm phạm về đời sống riêng tư, bí mật cá nhân và bí mật gia đình; có quyền bảo vệ danh dự, uy tín của mình.

Thông tin về đời sống riêng tư, bí mật cá nhân, bí mật gia đình được pháp luật bảo đảm an toàn.

2. Mọi người có quyền bí mật thư tín, điện thoại, điện tín và các hình thức trao đổi thông tin riêng tư khác.

Không ai được bóc mở, kiểm soát, thu giữ trái luật thư tín, điện thoại, điện tín và các hình thức trao đổi thông tin riêng tư của người khác.

Điều 22.

1. Công dân có quyền có nơi ở hợp pháp.

2. Mọi người có quyền bất khả xâm phạm về chỗ ở. Không ai được tự ý vào chỗ ở của người khác nếu không được người đó đồng ý.

3. Việc khám xét chỗ ở do luật định.

Điều 23.

Công dân có quyền tự do đi lại và cư trú ở trong nước, có quyền ra nước ngoài và từ nước ngoài về nước. Việc thực hiện các quyền này do pháp luật quy định.

Điều 24.

1. Mọi người có quyền tự do tín ngưỡng, tôn giáo, theo hoặc không theo một tôn giáo nào. Các tôn giáo bình đẳng trước pháp luật.

2. Nhà nước tôn trọng và bảo hộ quyền tự do tín ngưỡng, tôn giáo.

3. Không ai được xâm phạm tự do tín ngưỡng, tôn giáo hoặc lợi dụng tín ngưỡng, tôn giáo để vi phạm pháp luật.

Điều 25.

Công dân có quyền tự do ngôn luận, tự do báo chí, tiếp cận thông tin, hội họp, lập hội, biểu tình. Việc thực hiện các quyền này do pháp luật quy định.

Điều 26.

1. Công dân nam, nữ bình đẳng về mọi mặt. Nhà nước có chính sách bảo đảm quyền và cơ hội bình đẳng giới.

2. Nhà nước, xã hội và gia đình tạo điều kiện để phụ nữ phát triển toàn diện, phát huy vai trò của mình trong xã hội.

3. Nghiêm cấm phân biệt đối xử về giới.

Điều 27.

Công dân đủ mười tám tuổi trở lên có quyền bầu cử và đủ hai mươi mốt tuổi trở lên có quyền ứng cử vào Quốc hội, Hội đồng nhân dân. Việc thực hiện các quyền này do luật định.

Điều 28.

1. Công dân có quyền tham gia quản lý nhà nước và xã hội, tham gia thảo luận và kiến nghị với cơ quan nhà nước về các vấn đề của cơ sở, địa phương và cả nước.

2. Nhà nước tạo điều kiện để công dân tham gia quản lý nhà nước và xã hội; công khai, minh bạch trong việc tiếp nhận, phản hồi ý kiến, kiến nghị của công dân.

Điều 29.

Công dân đủ mười tám tuổi trở lên có quyền biểu quyết khi Nhà nước tổ chức trưng cầu ý dân.

Điều 30.

1. Mọi người có quyền khiếu nại, tố cáo với cơ quan, tổ chức, cá nhân có thẩm quyền về những việc làm trái pháp luật của cơ quan, tổ chức, cá nhân.

2. Cơ quan, tổ chức, cá nhân có thẩm quyền phải tiếp nhận, giải quyết khiếu nại, tố cáo. Người bị thiệt hại có quyền được bồi thường về vật chất, tinh thần và phục hồi danh dự theo quy định của pháp luật.

3. Nghiêm cấm việc trả thù người khiếu nại, tố cáo hoặc lợi dụng quyền khiếu nại, tố cáo để vu khống, vu cáo làm hại người khác.

Điều 31.

1. Người bị buộc tội được coi là không có tội cho đến khi được chứng minh theo trình tự luật định và có bản án kết tội của Tòa án đã có hiệu lực pháp luật.

2. Người bị buộc tội phải được Tòa án xét xử kịp thời trong thời hạn luật định, công bằng, công khai. Trường hợp xét xử kín theo quy định của luật thì việc tuyên án phải được công khai.

3. Không ai bị kết án hai lần vì một tội phạm.

4. Người bị bắt, tạm giữ, tạm giam, khởi tố, điều tra, truy tố, xét xử có quyền tự bào chữa, nhờ luật sư hoặc người khác bào chữa.

5. Người bị bắt, tạm giữ, tạm giam, khởi tố, điều tra, truy tố, xét xử, thi hành án trái pháp luật có quyền được bồi thường thiệt hại về vật chất, tinh thần và phục hồi danh dự. Người vi phạm pháp luật trong việc bắt, giam, giữ, khởi tố, điều tra, truy tố, xét xử, thi hành án gây thiệt hại cho người khác phải bị xử lý theo pháp luật.

Điều 32.

1. Mọi người có quyền sở hữu về thu nhập hợp pháp, của cải để dành, nhà ở, tư liệu sinh hoạt, tư liệu sản xuất, phần vốn góp trong doanh nghiệp hoặc trong các tổ chức kinh tế khác.

2. Quyền sở hữu tư nhân và quyền thừa kế được pháp luật bảo hộ.

3. Trường hợp thật cần thiết vì lý do quốc phòng, an ninh hoặc vì lợi ích quốc gia, tình trạng khẩn cấp, phòng, chống thiên tai, Nhà nước trưng mua hoặc trưng dụng có bồi thường tài sản của tổ chức, cá nhân theo giá thị trường.

Điều 33.

Mọi người có quyền tự do kinh doanh trong những ngành nghề mà pháp luật không cấm.

Điều 34.

Công dân có quyền được bảo đảm an sinh xã hội.

Điều 35.

1. Công dân có quyền làm việc, lựa chọn nghề nghiệp, việc làm và nơi làm việc.

2. Người làm công ăn lương được bảo đảm các điều kiện làm việc công bằng, an toàn; được hưởng lương, chế độ nghỉ ngơi.

3. Nghiêm cấm phân biệt đối xử, cưỡng bức lao động, sử dụng nhân công dưới độ tuổi lao động tối thiểu.

Điều 36.

1. Nam, nữ có quyền kết hôn, ly hôn. Hôn nhân theo nguyên tắc tự nguyện, tiến bộ, một vợ một chồng, vợ chồng bình đẳng, tôn trọng lẫn nhau.

2. Nhà nước bảo hộ hôn nhân và gia đình, bảo hộ quyền lợi của người mẹ và trẻ em.

Điều 37.

1. Trẻ em được Nhà nước, gia đình và xã hội bảo vệ, chăm sóc và giáo dục; được tham gia vào các vấn đề về trẻ em. Nghiêm cấm xâm hại, hành hạ, ngược đãi, bỏ mặc, lạm dụng, bóc lột sức lao động và những hành vi khác vi phạm quyền trẻ em.

2. Thanh niên được Nhà nước, gia đình và xã hội tạo điều kiện học tập, lao động, giải trí, phát triển thể lực, trí tuệ, bồi dưỡng đạo đức, truyền thống dân tộc, ý thức công dân; đi đầu trong công cuộc lao động sáng tạo và bảo vệ Tổ quốc.

3. Người cao tuổi được Nhà nước, gia đình và xã hội tôn trọng, chăm sóc và phát huy vai trò trong sự nghiệp xây dựng và bảo vệ Tổ quốc.

Điều 38.

1. Mọi người có quyền được bảo vệ, chăm sóc sức khỏe, bình đẳng trong việc sử dụng các dịch vụ y tế và có nghĩa vụ thực hiện các quy định về phòng bệnh, khám bệnh, chữa bệnh.

2. Nghiêm cấm các hành vi đe dọa cuộc sống, sức khỏe của người khác và cộng đồng.

Điều 39.

Công dân có quyền và nghĩa vụ học tập.

Điều 40.

Mọi người có quyền nghiên cứu khoa học và công nghệ, sáng tạo văn học, nghệ thuật và thụ hưởng lợi ích từ các hoạt động đó.

Điều 41.

Mọi người có quyền hưởng thụ và tiếp cận các giá trị văn hóa, tham gia vào đời sống văn hóa, sử dụng các cơ sở văn hóa.

Điều 42.

Công dân có quyền xác định dân tộc của mình, sử dụng ngôn ngữ mẹ đẻ, lựa chọn ngôn ngữ giao tiếp.

Điều 43.

Mọi người có quyền được sống trong môi trường trong lành và có nghĩa vụ bảo vệ môi trường.

Điều 44.

Công dân có nghĩa vụ trung thành với Tổ quốc.

Phản bội Tổ quốc là tội nặng nhất.

Điều 45.

1. Bảo vệ Tổ quốc là nghĩa vụ thiêng liêng và quyền cao quý của công dân.

2. Công dân phải thực hiện nghĩa vụ quân sự và tham gia xây dựng nền quốc phòng toàn dân.

Điều 46.

Công dân có nghĩa vụ tuân theo Hiến pháp và pháp luật; tham gia bảo vệ an ninh quốc gia, trật tự, an toàn xã hội và chấp hành những quy tắc sinh hoạt công cộng.

Điều 47.

Mọi người có nghĩa vụ nộp thuế theo luật định.

Điều 48.

Người nước ngoài cư trú ở Việt Nam phải tuân theo Hiến pháp và pháp luật Việt Nam; được bảo hộ tính mạng, tài sản và các quyền, lợi ích chính đáng theo pháp luật Việt Nam.

Điều 49.

Người nước ngoài đấu tranh vì tự do và độc lập dân tộc, vì chủ nghĩa xã hội, dân chủ và hòa bình hoặc vì sự nghiệp khoa học mà bị bức hại thì được Nhà nước Cộng hòa xã hội chủ nghĩa Việt Nam xem xét cho cư trú.

Chương III.

KINH TẾ, XÃ HỘI, VĂN HÓA, GIÁO DỤC, KHOA HỌC, CÔNG NGHỆ VÀ MÔI TRƯỜNG

Điều 50.

Nước Cộng hòa xã hội chủ nghĩa Việt Nam xây dựng nền kinh tế độc lập, tự chủ, phát huy nội lực, hội nhập, hợp tác quốc tế, gắn kết chặt chẽ với phát triển văn hóa, thực hiện tiến bộ và công bằng xã hội, bảo vệ môi trường, thực hiện công nghiệp hóa, hiện đại hóa đất nước.

Điều 51.

1. Nền kinh tế Việt Nam là nền kinh tế thị trường định hướng xã hội chủ nghĩa với nhiều hình thức sở hữu, nhiều thành phần kinh tế; kinh tế nhà nước giữ vai trò chủ đạo.

2. Các thành phần kinh tế đều là bộ phận cấu thành quan trọng của nền kinh tế quốc dân. Các chủ thể thuộc các thành phần kinh tế bình đẳng, hợp tác và cạnh tranh theo pháp luật.

3. Nhà nước khuyến khích, tạo điều kiện để doanh nhân, doanh nghiệp và cá nhân, tổ chức khác đầu tư, sản xuất, kinh doanh; phát triển bền vững các ngành kinh tế, góp phần xây dựng đất nước. Tài sản hợp pháp của cá nhân, tổ chức đầu tư, sản xuất, kinh doanh được pháp luật bảo hộ và không bị quốc hữu hóa.

Điều 52.

Nhà nước xây dựng và hoàn thiện thể chế kinh tế, điều tiết nền kinh tế trên cơ sở tôn trọng các quy luật thị trường; thực hiện phân công, phân cấp, phân quyền trong quản lý nhà nước; thúc đẩy liên kết kinh tế vùng, bảo đảm tính thống nhất của nền kinh tế quốc dân.

Điều 53.

Đất đai, tài nguyên nước, tài nguyên khoáng sản, nguồn lợi ở vùng biển, vùng trời, tài nguyên thiên nhiên khác và các tài sản do Nhà nước đầu tư, quản lý là tài sản công thuộc sở hữu toàn dân do Nhà nước đại diện chủ sở hữu và thống nhất quản lý.

Điều 54.

1. Đất đai là tài nguyên đặc biệt của quốc gia, nguồn lực quan trọng phát triển đất nước, được quản lý theo pháp luật.

2. Tổ chức, cá nhân được Nhà nước giao đất, cho thuê đất, công nhận quyền sử dụng đất. Người sử dụng đất được chuyển quyền sử dụng đất, thực hiện các quyền và nghĩa vụ theo quy định của luật. Quyền sử dụng đất được pháp luật bảo hộ.

3. Nhà nước thu hồi đất do tổ chức, cá nhân đang sử dụng trong trường hợp thật cần thiết do luật định vì mục đích quốc phòng, an ninh; phát triển kinh tế - xã hội vì lợi ích quốc gia, công cộng. Việc thu hồi đất phải công khai, minh bạch và được bồi thường theo quy định của pháp luật.

4. Nhà nước trưng dụng đất trong trường hợp thật cần thiết do luật định để thực hiện nhiệm vụ quốc phòng, an ninh hoặc trong tình trạng chiến tranh, tình trạng khẩn cấp, phòng, chống thiên tai.

Điều 55.

1. Ngân sách nhà nước, dự trữ quốc gia, quỹ tài chính nhà nước và các nguồn tài chính công khác do Nhà nước thống nhất quản lý và phải được sử dụng hiệu quả, công bằng, công khai, minh bạch, đúng pháp luật.

2. Ngân sách nhà nước gồm ngân sách trung ương và ngân sách địa phương, trong đó ngân sách trung ương giữ vai trò chủ đạo, bảo đảm nhiệm vụ chi của quốc gia. Các khoản thu, chi ngân sách nhà nước phải được dự toán và do luật định.

3. Đơn vị tiền tệ quốc gia là Đồng Việt Nam. Nhà nước bảo đảm ổn định giá trị đồng tiền quốc gia.

Điều 56.

Cơ quan, tổ chức, cá nhân phải thực hành tiết kiệm, chống lãng phí, phòng, chống tham nhũng trong hoạt động kinh tế - xã hội và quản lý nhà nước.

Điều 57.

1. Nhà nước khuyến khích, tạo điều kiện để tổ chức, cá nhân tạo việc làm cho người lao động.

2. Nhà nước bảo vệ quyền, lợi ích hợp pháp của người lao động, người sử dụng lao động và tạo điều kiện xây dựng quan hệ lao động tiến bộ, hài hòa và ổn định.

Điều 58.

1. Nhà nước, xã hội đầu tư phát triển sự nghiệp bảo vệ, chăm sóc sức khỏe của Nhân dân, thực hiện bảo hiểm y tế toàn dân, có chính sách ưu tiên chăm sóc sức khoẻ cho đồng bào dân tộc thiểu số, đồng bào ở miền núi, hải đảo và vùng có điều kiện kinh tế - xã hội đặc biệt khó khăn.

2. Nhà nước, xã hội và gia đình có trách nhiệm bảo vệ, chăm sóc sức khỏe người mẹ, trẻ em, thực hiện kế hoạch hóa gia đình.

Điều 59.

1. Nhà nước, xã hội tôn vinh, khen thưởng, thực hiện chính sách ưu đãi đối với người có công với nước.

2. Nhà nước tạo bình đẳng về cơ hội để công dân thụ hưởng phúc lợi xã hội, phát triển hệ thống an sinh xã hội, có chính sách trợ giúp người cao tuổi, người khuyết tật, người nghèo và người có hoàn cảnh khó khăn khác.

3. Nhà nước có chính sách phát triển nhà ở, tạo điều kiện để mọi người có chỗ ở.

Điều 60.

1. Nhà nước, xã hội chăm lo xây dựng và phát triển nền văn hóa Việt Nam tiên tiến, đậm đà bản sắc dân tộc, tiếp thu tinh hoa văn hóa nhân loại.

2. Nhà nước, xã hội phát triển văn học, nghệ thuật nhằm đáp ứng nhu cầu tinh thần đa dạng và lành mạnh của Nhân dân; phát triển các phương tiện thông tin đại chúng nhằm đáp ứng nhu cầu thông tin của Nhân dân, phục vụ sự nghiệp xây dựng và bảo vệ Tổ quốc.

3. Nhà nước, xã hội tạo môi trường xây dựng gia đình Việt Nam ấm no, tiến bộ, hạnh phúc; xây dựng con người Việt Nam có sức khỏe, văn hóa, giàu lòng yêu nước, có tinh thần đoàn kết, ý thức làm chủ, trách nhiệm công dân.

Điều 61.

1. Phát triển giáo dục là quốc sách hàng đầu nhằm nâng cao dân trí, phát triển nguồn nhân lực, bồi dưỡng nhân tài.

2. Nhà nước ưu tiên đầu tư và thu hút các nguồn đầu tư khác cho giáo dục; chăm lo giáo dục mầm non; bảo đảm giáo dục tiểu học là bắt buộc, Nhà nước không thu học phí; từng bước phổ cập giáo dục trung học; phát triển giáo dục đại học, giáo dục nghề nghiệp; thực hiện chính sách học bổng, học phí hợp lý.

3. Nhà nước ưu tiên phát triển giáo dục ở miền núi, hải đảo, vùng đồng bào dân tộc thiểu số và vùng có điều kiện kinh tế - xã hội đặc biệt khó khăn; ưu tiên sử dụng, phát triển nhân tài; tạo điều kiện để người khuyết tật và người nghèo được học văn hóa và học nghề.

Điều 62.

1. Phát triển khoa học và công nghệ là quốc sách hàng đầu, giữ vai trò then chốt trong sự nghiệp phát triển kinh tế - xã hội của đất nước.

2. Nhà nước ưu tiên đầu tư và khuyến khích tổ chức, cá nhân đầu tư nghiên cứu, phát triển, chuyển giao, ứng dụng có hiệu quả thành tựu khoa học và công nghệ; bảo đảm quyền nghiên cứu khoa học và công nghệ; bảo hộ quyền sở hữu trí tuệ.

3. Nhà nước tạo điều kiện để mọi người tham gia và được thụ hưởng lợi ích từ các hoạt động khoa học và công nghệ.

Điều 63.

1. Nhà nước có chính sách bảo vệ môi trường; quản lý, sử dụng hiệu quả, bền vững các nguồn tài nguyên thiên nhiên; bảo tồn thiên nhiên, đa dạng sinh học; chủ động phòng, chống thiên tai, ứng phó với biến đổi khí hậu.

2. Nhà nước khuyến khích mọi hoạt động bảo vệ môi trường, phát triển, sử dụng năng lượng mới, năng lượng tái tạo.

3. Tổ chức, cá nhân gây ô nhiễm môi trường, làm suy kiệt tài nguyên thiên nhiên và suy giảm đa dạng sinh học phải bị xử lý nghiêm và có trách nhiệm khắc phục, bồi thường thiệt hại.
            ''',
        },
    ],
    temperature=0,
    max_tokens=512,
)

message = response.choices[0].message.content
print(f"{message}")

# system_content = "You are a travel agent. Be descriptive and helpful."
# user_content = "Tell me about San Francisco"

# stream = client.chat.completions.create(
#     model="meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
#     messages=[
#         {"role": "system", "content": system_content},
#         {"role": "user", "content": user_content},
#     ],
#     stream=True,
#     max_tokens=512,
# )
# for chunk in stream:
#     print(chunk.choices[0].message.content or "", end="", flush=True)