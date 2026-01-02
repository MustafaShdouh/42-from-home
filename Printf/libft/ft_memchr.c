/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/09 18:15:41 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/30 20:13:08 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
//#include <string.h>
//#include <stddef.h>
#include "libft.h"

void	*ft_memchr(const void *s, int c, size_t n)
{
	size_t			i;
	unsigned char	*edit;

	i = 0;
	edit = (unsigned char *)s;
	while (i < n)
	{
		if (edit[i] == (unsigned char)c)
		{
			return ((unsigned char *)&edit[i]);
		}
		i++;
	}
	return (0);
}

/*int	main(void)
{
	const void	*s = "Hello World";
	char *myPtr1 = (char*)ft_memchr(s, 'o', 5);
	printf("%s\n", myPtr1);
    char *myPtr2 = (char*)memchr(s, 'o', 4);
    printf("%s\n", myPtr2);

}*/
