/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memset.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/09 17:44:38 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/30 20:43:01 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
//#include <string.h>
#include "libft.h"

void	*ft_memset(void *s, int c, size_t n)
{
	size_t			i;
	unsigned char	*edit;

	edit = (unsigned char *)s;
	i = 0;
	while (i < n)
	{
		edit[i] = (unsigned char)c;
		i++;
	}
	return (s);
}

/*int	main(void)
{
	char	buffer[10] = {};
	ft_memset(buffer, 2, 5);
	for (int i = 0; i < 10; i++) {
        printf("%d ", buffer[i]);
    }
	printf("\n");
	memset(buffer, 2, 5);
        for (int i = 0; i < 10; i++) {
        printf("%d ", buffer[i]);
    }

}*/
